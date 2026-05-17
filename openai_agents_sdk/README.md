# Building Multi-Agent Systems with OpenAI Agents SDK

This folder contains a hands-on workshop for building agentic applications with the OpenAI Agents SDK.

## Projects

1. **Deep Research Agent**
   - Uses the official OpenAI Agents SDK research bot architecture: planner agent, parallel search agents, writer agent, `WebSearchTool`, streaming, and tracing.
   - Notebook: `notebooks/01_deep_research_agent.ipynb`

2. **Voice Interview Agent**
   - Builds a voice-based mock interview agent using official voice workflows, `WebSearchTool`, `CodeInterpreterTool`, handoffs, TTS tuning, and streamed audio.
   - Notebook: `notebooks/02_job_interview_agent.ipynb`

## Setup

Each notebook installs dependencies directly:

```python
!pip install -q openai-agents[voice] python-dotenv numpy sounddevice
```

Each notebook loads `OPENAI_API_KEY` from the repo root `.env` file:

```python
from dotenv import load_dotenv

load_dotenv("../../.env")
```

## Local Setup

```bash
pip install -r requirements.txt
```

## Functional Demo App

A browser-based demo for the two workshop agents is available at `../demo-app/`.

It includes:

- An IndiGo customer service chatbot with FAQ retrieval, handoffs, shared booking context, and guardrails.
- An OpenAI AI Agents Engineer voice interview demo with microphone input, transcription, interviewer audio, and a live transcript UI.

Run it from the repository root:

```bash
cd demo-app
pip install -r requirements.txt
uvicorn main:app --reload
```

## Workshop Flow

- Run the notebooks in order for a progressive experience.
- Each notebook is also self-contained and can be taught independently.
- Keep explanations short during delivery and let the code drive the session.
