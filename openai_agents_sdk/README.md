# Building Multi-Agent Systems with OpenAI Agents SDK

This folder contains a 90-minute hands-on workshop made of three self-contained 30-minute Colab notebooks.

## Projects

1. **Deep Research Agent**
   - Builds a research agent with `Agent`, `Runner`, `WebSearchTool`, custom tools, and structured output.
   - Notebook: `notebooks/01_deep_research_agent.ipynb`

2. **Resume Job Fit Analyzer**
   - Builds a multi-agent hiring pipeline with handoffs, parallel orchestration, dynamic instructions, cloning, chaining, and structured reports.
   - Notebook: `notebooks/02_resume_job_fit_analyzer.ipynb`

3. **GitHub Copilot with MCP**
   - Builds an engineering copilot that uses DeepWiki MCP, input guardrails, output guardrails, and tracing.
   - Notebook: `notebooks/03_github_copilot_mcp.ipynb`

## Setup

Each notebook installs dependencies directly:

```python
!pip install -q openai-agents python-dotenv
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

## Workshop Flow

- Run the notebooks in order for a progressive experience.
- Each notebook is also self-contained and can be taught independently.
- Keep explanations short during delivery and let the code drive the session.
