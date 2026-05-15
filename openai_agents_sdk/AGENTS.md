# AGENTS.md

Guidance for agents working in this workshop folder.

## Scope

These instructions apply to files under `openai_agents_sdk/`.

## Workshop Style

- Keep notebooks minimal: short section headers, readable code, and very little prose.
- Each notebook should remain self-contained and runnable in Colab.
- Prefer simple examples that fit a 30-minute live workshop.
- Avoid adding tests unless explicitly requested.
- Do not create Jupyter notebooks outside the existing `notebooks/` folder.

## Notebook Conventions

- Use `!pip install -q openai-agents python-dotenv` for text notebooks.
- Use `!pip install -q openai-agents[voice] python-dotenv numpy sounddevice` for voice notebooks.
- Load `OPENAI_API_KEY` from the repo root `.env` with `load_dotenv("../../.env")`.
- Keep project code in notebook cells rather than helper modules unless explicitly requested.
- Use structured outputs with Pydantic where they make the result easier to inspect.
- Avoid complex abstractions when plain Python orchestration is easier to teach.

## Project Boundaries

- Project 1: Deep Research Agent.
- Project 2: Voice Interview Agent.

Do not reintroduce old projects (code review, resume analyzer, GitHub copilot) unless explicitly requested.
