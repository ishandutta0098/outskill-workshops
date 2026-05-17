# Outskill Workshops Demo App

Functional UI demos for the OpenAI Agents SDK workshop notebooks.

## Demos

- `IndiGo Assistant` shows the customer service chatbot from `openai_agents_sdk/notebooks/01_customer_service_chatbot.ipynb`.
- `OpenAI Assessment` shows the audio-to-audio interview flow from `openai_agents_sdk/notebooks/02_job_interview_agent.ipynb`.

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000`.

## Pages

- `/` — AI agent showcase home
- `/indigo.html` — IndiGo assistant landing page
- `/indigo-chat.html` — IndiGo chatbot
- `/assessment.html` — OpenAI assessment dashboard
- `/interview.html` — live voice interview UI

## APIs

- `POST /api/indigo/chat`
- `POST /api/interview/start`
- `POST /api/interview/message`
- `POST /api/interview/voice`
- `POST /api/tts`
