import asyncio
import uuid
from openai import OpenAI
from agents import (
    Agent,
    Runner,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    WebSearchTool,
    FileSearchTool,
    CodeInterpreterTool,
    handoff,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

_resume_store_id: str | None = None

JOB_DESCRIPTION = """
AI Agents SDK Engineer — OpenAI

You will join the OpenAI Agents SDK team to design, build, and teach the patterns
developers use to create production-grade AI agents.

Responsibilities:
- Architect multi-agent orchestration patterns: routing, handoffs, and shared context
- Build and maintain hosted tools: FileSearchTool, WebSearchTool, CodeInterpreterTool, and custom @function_tool integrations
- Implement voice-capable agents using VoicePipeline and SingleAgentVoiceWorkflow
- Enforce output grounding with ModelSettings(tool_choice="required")
- Write developer documentation, tutorials, and workshop notebooks

Requirements:
- Strong Python with experience designing developer-facing SDKs or APIs
- Hands-on experience building agents with tool calling, handoffs, and context management
- Familiarity with vector stores, embeddings, and document retrieval (FileSearchTool / RAG)
- Experience with voice interfaces, audio pipelines, or real-time streaming
- Understanding of structured outputs, Pydantic models, and multi-agent evaluation
"""

VOICE_RULES = f"""
You are conducting a text-based mock interview. Keep every response concise (under 100 words).
Ask one question at a time. Do not use bullet points in spoken questions.

You are interviewing for this role:
{JOB_DESCRIPTION}
"""


def _build_interview_agents(resume_store_id: str | None) -> Agent:
    tools = [WebSearchTool()]
    if resume_store_id:
        tools.append(FileSearchTool(vector_store_ids=[resume_store_id]))
    tools.append(
        CodeInterpreterTool(
            tool_config={"type": "code_interpreter", "container": {"type": "auto"}},
        )
    )

    feedback_agent = Agent(
        name="FeedbackAgent",
        handoff_description="Gives the final interview scorecard.",
        model="gpt-4o",
        instructions=VOICE_RULES + """
Use CodeInterpreterTool if you need to calculate or aggregate a score.
Create a concise final scorecard for the AI Agents Engineer interview.
Mention one strength, one improvement area, and an overall score out of 5.
""",
        tools=tools,
    )

    questioner_agent = Agent(
        name="QuestionerAgent",
        handoff_description="Asks AI agents interview questions and evaluates answers.",
        model="gpt-4o",
        instructions=prompt_with_handoff_instructions(VOICE_RULES + """
You ask beginner-friendly AI Agents Engineer questions one at a time.
Use WebSearchTool for current role expectations if needed.
For each candidate answer, give one short evaluation sentence, then ask the next question.
After 4 questions or if the candidate says they want to stop or finish, hand off to FeedbackAgent.
"""),
        tools=tools,
        handoffs=[feedback_agent],
    )

    greeter_agent = Agent(
        name="GreeterAgent",
        handoff_description="Starts the interview and routes to the questioner.",
        model="gpt-4o",
        instructions=prompt_with_handoff_instructions(VOICE_RULES + """
Greet the candidate warmly, explain this is an AI Agents Engineer interview for OpenAI,
then immediately hand off to QuestionerAgent to begin.
"""),
        tools=[WebSearchTool()],
        handoffs=[questioner_agent],
    )

    return greeter_agent


def get_greeter_agent() -> Agent:
    return _build_interview_agents(_resume_store_id)


def _init_resume_store_sync(pdf_path: str) -> str:
    client = OpenAI()

    with open(pdf_path, "rb") as f:
        uploaded_resume = client.files.create(file=f, purpose="assistants")

    resume_store = client.vector_stores.create(name="Candidate Resume")
    client.vector_stores.files.create(
        vector_store_id=resume_store.id,
        file_id=uploaded_resume.id,
    )

    import time
    while True:
        files = client.vector_stores.files.list(vector_store_id=resume_store.id).data
        if files and files[0].status == "completed":
            break
        time.sleep(1)

    return resume_store.id


async def init_resume_store(pdf_path: str) -> None:
    global _resume_store_id
    store_id = await asyncio.to_thread(_init_resume_store_sync, pdf_path)
    _resume_store_id = store_id
    print(f"Resume vector store ready: {_resume_store_id}")


_sessions: dict[str, dict] = {}

STOP_PHRASES = {"stop", "exit", "quit", "goodbye", "end interview", "finish", "that's all"}


async def start_session() -> dict:
    session_id = str(uuid.uuid4())
    greeter = get_greeter_agent()

    result = await Runner.run(greeter, "Hello, I'm ready to start the interview.")

    history = result.to_input_list()
    last_agent = greeter
    greeting = ""
    handoffs_seen = []

    for item in result.new_items:
        if isinstance(item, HandoffOutputItem):
            handoffs_seen.append(f"{item.source_agent.name} → {item.target_agent.name}")
            last_agent = item.target_agent
        elif isinstance(item, MessageOutputItem):
            text = ItemHelpers.text_message_output(item)
            if text:
                greeting = text
                last_agent = item.agent

    _sessions[session_id] = {
        "current_agent": last_agent,
        "history": history,
        "question_count": 0,
        "ended": False,
    }

    return {
        "session_id": session_id,
        "reply": greeting,
        "agent": last_agent.name,
        "handoffs": handoffs_seen,
        "ended": False,
    }


async def send_message(session_id: str, user_text: str) -> dict:
    session = _sessions.get(session_id)
    if not session:
        return {"error": "Session not found", "ended": True}

    if session["ended"]:
        return {"reply": "This interview session has ended.", "agent": "System", "ended": True}

    current_agent = session["current_agent"]
    history = session["history"] + [{"role": "user", "content": user_text}]

    result = await Runner.run(current_agent, history)

    new_history = result.to_input_list()
    last_agent = current_agent
    reply = ""
    handoffs_seen = []

    for item in result.new_items:
        if isinstance(item, HandoffOutputItem):
            handoffs_seen.append(f"{item.source_agent.name} → {item.target_agent.name}")
            last_agent = item.target_agent
        elif isinstance(item, MessageOutputItem):
            text = ItemHelpers.text_message_output(item)
            if text:
                reply = text
                last_agent = item.agent

    ended = last_agent.name == "FeedbackAgent" and any(
        phrase in user_text.lower() for phrase in STOP_PHRASES
    )
    if last_agent.name == "FeedbackAgent" and not ended:
        ended = session["question_count"] >= 4

    session["current_agent"] = last_agent
    session["history"] = new_history
    session["question_count"] += 1
    session["ended"] = ended

    return {
        "reply": reply,
        "agent": last_agent.name,
        "handoffs": handoffs_seen,
        "ended": ended,
    }
