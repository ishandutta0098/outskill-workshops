# Workshop Contents — OpenAI Agents SDK

## What We Cover

### Notebook 1: Customer Service Chatbot (IndiGo Airlines)
1. **Basic Agent** — Create an agent with plain instructions and no tools
2. **Custom Tools** — Add a `@function_tool` to look up FAQs; explore `FileSearchTool` with a real PDF policy document
3. **Multiple Agents + Handoffs** — Build a triage agent that routes customers to specialist agents (FAQ, seat booking)
4. **Shared Context** — Pass a typed Pydantic context object across agents and tools to persist state across turns

### Notebook 2: Voice Interview Agent (AI Agents Engineer Role)
1. **VoicePipeline Basics** — Audio in → STT → Agent → TTS → Audio out with `SingleAgentVoiceWorkflow`
2. **Memory & Multi-Turn** — Reuse a workflow instance to maintain conversation history; hook into transcription with `SingleAgentWorkflowCallbacks`
3. **Tools in Voice** — Plug in `WebSearchTool`, `FileSearchTool` (resume PDF), and `CodeInterpreterTool` into a voice agent
4. **Handoffs** — Chain Greeter → Questioner → Feedback agents with seamless voice transitions
5. **Full Interview System** — Custom `VoiceWorkflowBase` subclass, `TTSModelSettings` for voice tuning, stop-phrase detection, and a live streamed scorecard

---

## Learner Outcomes

By the end of this workshop you will be able to:

- Build a working multi-agent system from scratch using the OpenAI Agents SDK
- Create and register custom tools with `@function_tool` and use hosted tools (`FileSearchTool`, `WebSearchTool`, `CodeInterpreterTool`)
- Design agent pipelines with handoffs and a triage router
- Share typed state across agents using `RunContextWrapper` and Pydantic models
- Wire up a full voice agent pipeline with multi-turn memory, tool use, and handoffs
- Tune TTS delivery and control the interview flow with a custom `VoiceWorkflowBase`
