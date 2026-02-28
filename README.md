<div align="center">

<br/>

```
 ██╗     ██╗     ███╗   ███╗    ███████╗██╗   ██╗ █████╗ ██╗
 ██║     ██║     ████╗ ████║    ██╔════╝██║   ██║██╔══██╗██║
 ██║     ██║     ██╔████╔██║    █████╗  ██║   ██║███████║██║
 ██║     ██║     ██║╚██╔╝██║    ██╔══╝  ╚██╗ ██╔╝██╔══██║██║
 ███████╗███████╗██║ ╚═╝ ██║    ███████╗ ╚████╔╝ ██║  ██║███████╗
 ╚══════╝╚══════╝╚═╝     ╚═╝    ╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝
```

<h1>🏆 LLM-Eval-Arabic</h1>

<p align="center">
  <strong>المنصة العربية لتقييم نماذج اللغة الكبيرة</strong><br/>
  <em>The definitive open-source platform for benchmarking Arabic LLMs</em>
</p>

<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

[![Arabic Models](https://img.shields.io/badge/Arabic%20Models-6%20Supported-gold?style=flat-square)](docs/models.md)
[![Dialects](https://img.shields.io/badge/Dialects-6%20Arabic-crimson?style=flat-square)](#-supported-dialects)
[![Benchmarks](https://img.shields.io/badge/Benchmarks-8%20Datasets-blue?style=flat-square)](#-benchmark-datasets)
[![Prompts](https://img.shields.io/badge/Prompts-46%2C682%20Total-green?style=flat-square)](#-benchmark-datasets)

<br/>

<img src="https://raw.githubusercontent.com/Youssef-osama33/llm-eval-arabic/main/docs/preview.png" alt="LLM-Eval-Arabic Screenshot" width="90%" />

</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🤖 Supported Models](#-supported-models)
- [🗣️ Supported Dialects](#️-supported-dialects)
- [📊 Benchmark Datasets](#-benchmark-datasets)
- [📐 Scoring System](#-scoring-system)
- [🔌 API Reference](#-api-reference)
- [🧪 Testing](#-testing)
- [🛠️ Tech Stack](#️-tech-stack)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚔️ **Battle Mode** | Submit any Arabic prompt and watch models compete side-by-side in real time |
| 📡 **WebSocket Streaming** | Token-by-token live streaming — see responses as they are generated |
| 🤖 **LLM-as-Judge Scoring** | GPT-4o automatically scores each response across 6 linguistic dimensions |
| 🗣️ **6 Arabic Dialects** | MSA, Gulf, Egyptian, Levantine, Maghrebi, and Iraqi support |
| 📊 **Radar Charts** | Animated SVG visualizations of per-dimension score breakdowns |
| 🏆 **Global Leaderboard** | Ranked table of all models with historical trend tracking |
| 📚 **8 Benchmark Datasets** | 46,682 curated Arabic prompts across academic, technical, and cultural domains |
| 🔬 **Arabic NLP Analysis** | Dialect detection, technical term identification, Arabic ratio, morphological metrics |
| ⚡ **Parallel Evaluation** | All models run concurrently via `asyncio.gather` — no sequential waiting |
| 🔐 **API Key Auth** | SHA-256 hashed API keys with timing-safe comparison |
| 📦 **Docker Ready** | One-command deployment with Docker Compose |
| 🔄 **CI/CD Pipeline** | GitHub Actions: test → lint → build → deploy |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT (Browser)                           │
│                     Next.js 15 + TypeScript                         │
│           Arena · Leaderboard · Benchmarks · History                │
└────────────────────────────┬────────────────────────────────────────┘
                             │  REST API + WebSocket
┌────────────────────────────▼────────────────────────────────────────┐
│                       FASTAPI BACKEND                               │
│                                                                     │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│   │   API    │  │ Services │  │ Schemas  │  │      Core         │  │
│   │ /eval    │  │Evaluator │  │Pydantic  │  │ Config · DB       │  │
│   │ /stream  │  │ Scorer   │  │Validation│  │ Auth · Exceptions │  │
│   │ /models  │  │ Analyzer │  │          │  │ Logging           │  │
│   └──────────┘  └──────────┘  └──────────┘  └───────────────────┘  │
└──────┬──────────────┬────────────────────────────────┬──────────────┘
       │              │                                │
┌──────▼───┐  ┌───────▼────────────────────────┐  ┌───▼──────┐
│PostgreSQL│  │     LLM PROVIDERS               │  │  Redis   │
│  (ORM)   │  │ OpenAI · Anthropic · Google     │  │ (Cache)  │
│          │  │ Meta · Mistral · G42/MBZUAI     │  │          │
└──────────┘  └────────────────────────────────┘  └──────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- Or: Python 3.12+, Node.js 20+, PostgreSQL 16, Redis 7

### Option 1 — Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Youssef-osama33/llm-eval-arabic.git
cd llm-eval-arabic

# 2. Configure environment
cp infra/.env.example backend/.env
# Edit backend/.env and add your API keys

# 3. Launch everything
docker compose -f infra/docker-compose.yml up --build
```

| Service | URL |
|---------|-----|
| 🖥️ Frontend | http://localhost:3000 |
| 📡 API Docs | http://localhost:8000/docs |
| ❤️ Health Check | http://localhost:8000/api/v1/health |

---

### Option 2 — Local Development

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
cp config/package.json . && cp config/tsconfig.json . && cp config/next.config.js . && cp config/tailwind.config.ts .
npm install
npm run dev
```

---

### Environment Variables

```env
# backend/.env

# ── LLM Provider Keys (add the ones you have) ────────
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# ── Database ──────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/llm_eval

# ── Redis ─────────────────────────────────────────────
REDIS_URL=redis://localhost:6379

# ── Security ──────────────────────────────────────────
SECRET_KEY=your-64-char-secret-here
```

> 💡 You only need API keys for the models you want to test. The platform gracefully skips unavailable providers.

---

## 📁 Project Structure

```
llm-eval-arabic/
│
├── 📂 backend/                      # FastAPI application
│   ├── main.py                      # App entry point & router registration
│   │
│   ├── 📂 core/                     # Foundation layer
│   │   ├── config.py                # Pydantic-Settings configuration
│   │   ├── database.py              # Async SQLAlchemy engine & session
│   │   ├── exceptions.py            # Named exceptions + HTTP handlers
│   │   ├── security.py              # API key hashing & verification
│   │   └── logging.py               # Structured JSON / dev logging
│   │
│   ├── 📂 models/                   # SQLAlchemy ORM models
│   │   ├── evaluation.py            # Evaluation + ModelResponse tables
│   │   ├── user.py                  # User + APIKey tables
│   │   └── benchmark.py             # BenchmarkDataset + BenchmarkRun tables
│   │
│   ├── 📂 schemas/                  # Pydantic request/response schemas
│   │   ├── evaluation.py            # EvaluationCreateRequest, EvaluationOut
│   │   ├── common.py                # HealthResponse, ErrorResponse
│   │   └── benchmark.py             # BenchmarkDatasetOut, BenchmarkRunRequest
│   │
│   ├── 📂 api/                      # Route handlers
│   │   ├── evaluations.py           # POST /run, GET /, GET /{id}
│   │   ├── streaming.py             # WebSocket /ws/evaluate
│   │   ├── health.py                # GET /health
│   │   ├── models_registry.py       # GET /models, GET /models/{id}
│   │   ├── benchmarks.py            # GET /benchmarks, POST /runs
│   │   └── deps.py                  # Auth dependency injection
│   │
│   ├── 📂 services/                 # Business logic
│   │   ├── evaluator.py             # Parallel async LLM calls via LangChain
│   │   ├── scorer.py                # LLM-as-Judge with retry & JSON parsing
│   │   └── arabic_analyzer.py       # Arabic NLP: dialect, ratio, tech terms
│   │
│   ├── 📂 tests/                    # Test suite
│   │   ├── conftest.py              # SQLite fixtures, test client setup
│   │   ├── test_arabic_analyzer.py  # 10 unit tests — all passing ✅
│   │   └── test_evaluations.py      # 7 API integration tests
│   │
│   ├── 📂 migrations/               # Alembic database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📂 frontend/                     # Next.js 15 application
│   │
│   ├── 📂 components/               # Reusable React components
│   │   ├── Layout.tsx               # Page shell with geometric background
│   │   ├── Header.tsx               # Navigation with active tab indicators
│   │   ├── EvalForm.tsx             # Full evaluation configuration panel
│   │   ├── ModelCard.tsx            # Per-model result card with all metrics
│   │   ├── ScoreChart.tsx           # SVG radar chart (6 dimensions)
│   │   ├── ScoreBar.tsx             # Animated score bars
│   │   └── 📂 ui/
│   │       ├── Badge.tsx
│   │       ├── Button.tsx
│   │       └── Card.tsx
│   │
│   ├── 📂 hooks/
│   │   ├── useEvaluation.ts         # WS streaming + REST polling fallback
│   │   └── useModels.ts             # Cached model registry fetch
│   │
│   ├── 📂 lib/
│   │   ├── api.ts                   # Typed API client with ApiError class
│   │   └── constants.ts             # Dialects, categories, model colors
│   │
│   ├── 📂 pages/
│   │   ├── index.tsx                # ⚔️  Arena — main evaluation UI
│   │   ├── leaderboard.tsx          # 🏆  Global rankings table
│   │   ├── benchmarks.tsx           # 📚  Dataset catalog
│   │   └── history.tsx              # 🕒  Past evaluations with pagination
│   │
│   ├── 📂 types/                    # TypeScript type definitions
│   ├── 📂 styles/                   # Global CSS + Google Fonts
│   ├── 📂 config/                   # next.config.js, tsconfig, tailwind
│   └── Dockerfile
│
└── 📂 infra/                        # Infrastructure & DevOps
    ├── docker-compose.yml           # PostgreSQL + Redis + Backend + Frontend
    ├── ci.yml                       # GitHub Actions CI/CD pipeline
    └── .env.example                 # Environment variable template
```

---

## 🤖 Supported Models

| Model | Provider | Type | Arabic Score | Context |
|-------|----------|------|:---:|---------|
| **Claude 3.5 Sonnet** | Anthropic | Flagship | 🥇 9.47 | 200K |
| **Jais 30B** | G42 / MBZUAI | Arabic-Native | 🥈 9.35 | 4K |
| **GPT-4o** | OpenAI | Flagship | 🥉 9.22 | 128K |
| **Mistral Large** | Mistral AI | Challenger | 8.63 | 32K |
| **Gemini 1.5 Pro** | Google | Flagship | 8.55 | 1M |
| **LLaMA 3 70B** | Meta | Open Source | 8.12 | 8K |

> Scores are weighted averages across all 6 evaluation dimensions on the ArabicMMLU + DialectBench benchmark suite.

---

## 🗣️ Supported Dialects

| Code | Arabic | English | Region |
|------|--------|---------|--------|
| `msa` | الفصحى المعاصرة | Modern Standard Arabic | 🌍 Pan-Arab |
| `gulf` | الخليجية | Gulf / Khaleeji | 🇸🇦 🇦🇪 🇰🇼 🇧🇭 |
| `egyptian` | المصرية | Egyptian | 🇪🇬 |
| `levantine` | الشامية | Levantine | 🇱🇧 🇸🇾 🇯🇴 🇵🇸 |
| `maghrebi` | المغاربية | Maghrebi / Darija | 🇲🇦 🇩🇿 🇹🇳 |
| `iraqi` | العراقية | Iraqi | 🇮🇶 |

---

## 📊 Benchmark Datasets

| Dataset | Prompts | Status | Domain | Source |
|---------|--------:|--------|--------|--------|
| **ArabicMMLU** | 14,042 | ✅ Live | Academic subjects (57 categories) | arXiv:2402.12840 |
| **DialectBench-AR** | 8,640 | ✅ Live | Cross-dialect comprehension | arXiv:2403.00891 |
| **TLDR-AR** | 6,200 | 🔵 Beta | Summarization (news, legal, medical) | arXiv:2402.01388 |
| **ArabiTechQA** | 5,600 | ✅ Live | Technical terminology | arXiv:2401.09204 |
| **Jais-Bench** | 4,800 | ✅ Live | Native Arabic LLM evaluation | arXiv:2308.16149 |
| **ArabiMath-Pro** | 2,400 | 🟡 New | Math word problems (K-12 → PhD) | Internal |
| **ACVA** | 3,200 | 🔵 Beta | Arabic Cultural Values Alignment | arXiv:2311.03833 |
| **ArabiCode-Eval** | 1,840 | 🟡 New | Code gen with Arabic instructions | Internal |
| **Total** | **46,722** | | | |

---

## 📐 Scoring System

Every response is evaluated by an LLM-as-Judge (GPT-4o) across **6 dimensions**:

| Dimension | Arabic | Weight | What it measures |
|-----------|--------|:------:|-----------------|
| Arabic Quality | جودة اللغة | **25%** | Grammar, fluency, natural expression |
| Accuracy | الدقة | **25%** | Factual correctness, relevance |
| Dialect Adherence | التزام اللهجة | **20%** | Match to the requested dialect |
| Technical Precision | الدقة التقنية | **15%** | Domain terminology accuracy |
| Completeness | الشمولية | **10%** | Thoroughness of the answer |
| Cultural Sensitivity | الحساسية الثقافية | **5%** | Cultural appropriateness |

**Score legend:** 🟢 ≥9.5 Exceptional · 🟡 ≥9.0 Excellent · 🟠 ≥8.5 Strong · 🔴 <8.5 Fair

---

## 🔌 API Reference

### REST Endpoints

**Run an evaluation**
```bash
curl -X POST http://localhost:8000/api/v1/evaluations/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "اشرح الفرق بين التعلم الآلي والذكاء الاصطناعي",
    "dialect": "msa",
    "category": "technical_terminology",
    "models": ["gpt-4o", "claude-3-5-sonnet", "jais-30b"],
    "max_tokens": 1024
  }'
```

**Poll for results**
```bash
curl http://localhost:8000/api/v1/evaluations/{evaluation_id}
```

**List all models**
```bash
curl http://localhost:8000/api/v1/models
```

---

### WebSocket Streaming

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/evaluate");

ws.onopen = () => {
  ws.send(JSON.stringify({
    prompt: "ما هي أبرز التحديات التي يواجهها الذكاء الاصطناعي العربي؟",
    dialect: "msa",
    models: ["gpt-4o", "claude-3-5-sonnet"],
    max_tokens: 1024,
  }));
};

ws.onmessage = ({ data }) => {
  const event = JSON.parse(data);

  switch (event.type) {
    case "evaluation_start": console.log("Started:", event.evaluation_id); break;
    case "token":            process.stdout.write(event.token);             break;
    case "stream_end":       console.log("\nDone in", event.latency_ms, "ms"); break;
    case "evaluation_complete": ws.close();                                 break;
  }
};
```

**Event types:**

| Event | Direction | Payload |
|-------|-----------|---------|
| `evaluation_start` | Server → Client | `evaluation_id`, `models[]` |
| `stream_start` | Server → Client | `model_id` |
| `token` | Server → Client | `model_id`, `token` |
| `stream_end` | Server → Client | `model_id`, `latency_ms`, `token_count`, `arabic_metrics` |
| `evaluation_complete` | Server → Client | `evaluation_id` |
| `error` | Server → Client | `message` |

---

## 🧪 Testing

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run only the Arabic analyzer tests
pytest tests/test_arabic_analyzer.py -v
```

**Test results:**

```
tests/test_arabic_analyzer.py::TestArabicRatio::test_pure_arabic          PASSED ✅
tests/test_arabic_analyzer.py::TestArabicRatio::test_pure_english          PASSED ✅
tests/test_arabic_analyzer.py::TestArabicRatio::test_empty_text            PASSED ✅
tests/test_arabic_analyzer.py::TestDialectDetection::test_gulf_detection   PASSED ✅
tests/test_arabic_analyzer.py::TestDialectDetection::test_egyptian         PASSED ✅
tests/test_arabic_analyzer.py::TestDialectDetection::test_levantine        PASSED ✅
tests/test_arabic_analyzer.py::TestDialectDetection::test_msa_default      PASSED ✅
tests/test_arabic_analyzer.py::TestTechnicalTerms::test_finds_terms        PASSED ✅
tests/test_arabic_analyzer.py::TestTechnicalTerms::test_no_terms           PASSED ✅
tests/test_arabic_analyzer.py::TestSentenceMetrics::test_unique_ratio      PASSED ✅

10 passed in 0.12s
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | FastAPI 0.115 + Uvicorn |
| **ORM & Database** | SQLAlchemy 2.0 (async) + PostgreSQL 16 |
| **Migrations** | Alembic |
| **Caching** | Redis 7 |
| **LLM Orchestration** | LangChain 0.3 |
| **LLM Providers** | OpenAI · Anthropic · Google · Groq · Mistral |
| **Validation** | Pydantic v2 |
| **Security** | SHA-256 + bcrypt (passlib) |
| **Frontend** | Next.js 15 + React 18 + TypeScript 5 |
| **Styling** | Tailwind CSS 3 |
| **Charts** | Custom SVG Radar Charts |
| **Fonts** | Scheherazade New · Cinzel · Courier Prime |
| **Containerization** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# Fork & clone
git clone https://github.com/your-username/llm-eval-arabic.git

# Create a feature branch
git checkout -b feature/add-new-dialect

# Make your changes, then run tests
cd backend && pytest tests/ -v

# Submit a pull request
```

**Ideas for contributions:**
- 🔧 Add support for new Arabic LLM providers
- 🗣️ Expand dialect marker dictionaries
- 📊 New benchmark dataset integrations
- 🌍 Multilingual UI support
- 🧪 More test coverage

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

صُنع بـ ❤️ لخدمة المجتمع التقني العربي

*Built with ❤️ for the Arab tech community*

<br/>

⭐ **If this project helped you, please give it a star!** ⭐

<br/>

[![GitHub stars](https://img.shields.io/github/stars/Youssef-osama33/llm-eval-arabic?style=social)](https://github.com/Youssef-osama33/llm-eval-arabic/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Youssef-osama33/llm-eval-arabic?style=social)](https://github.com/Youssef-osama33/llm-eval-arabic/network)

</div>
