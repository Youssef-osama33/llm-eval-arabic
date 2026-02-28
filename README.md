# ⚔ LLM-Eval-Arabic

**The definitive open-source Arabic LLM evaluation platform.**

Compare GPT-4o, Claude, Gemini, Jais, LLaMA, and Mistral across 6 Arabic dialects with automated LLM-as-Judge scoring.

## Quick Start

```bash
git clone https://github.com/your-org/llm-eval-arabic
cd llm-eval-arabic
cp backend/.env.example backend/.env
# Edit .env and add your API keys
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/v1/health

## Project Structure

```
.
├── backend/                    # FastAPI + LangChain
│   ├── app/
│   │   ├── core/               # config, database, security, exceptions, logging
│   │   ├── models/             # SQLAlchemy ORM (evaluation, user, benchmark)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── api/                # Route handlers (evaluations, models, benchmarks, streaming, health)
│   │   ├── services/           # Business logic (evaluator, scorer, arabic_analyzer)
│   │   └── main.py             # FastAPI app entrypoint
│   ├── tests/                  # pytest tests with fixtures
│   ├── alembic/                # DB migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # Next.js 15 + TypeScript
│   └── src/
│       ├── components/         # Layout, Header, EvalForm, ModelCard, ScoreChart, ScoreBar
│       ├── hooks/              # useEvaluation, useModels
│       ├── lib/                # api client, constants
│       ├── pages/              # arena, leaderboard, benchmarks, history
│       └── types/              # TypeScript type definitions
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI 0.115, SQLAlchemy 2.0, LangChain 0.3 |
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16, Redis 7 |
| LLM Providers | OpenAI, Anthropic, Google, Groq, Mistral |
| Infra | Docker, GitHub Actions |

## API

```bash
# Run evaluation
curl -X POST http://localhost:8000/api/v1/evaluations/run \
  -H "Content-Type: application/json" \
  -d '{"prompt":"اشرح مفهوم التعلم الآلي","dialect":"msa","models":["gpt-4o","claude-3-5-sonnet"]}'

# Get result
curl http://localhost:8000/api/v1/evaluations/{id}

# WebSocket streaming
wscat -c ws://localhost:8000/ws/evaluate
```

## License

MIT
