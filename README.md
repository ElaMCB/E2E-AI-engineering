# E2E-AI-engineering

[![Portfolio](https://img.shields.io/badge/Portfolio-Live-blue?style=for-the-badge&logo=github)](https://elamcb.github.io/E2E-AI-engineering/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-January%202026-blue?style=for-the-badge)](https://github.com/ElaMCB/E2E-AI-engineering)

> **Note:** This repository uses branch protection. All changes must go through pull requests that pass CI checks.

[![CI](https://github.com/ElaMCB/E2E-AI-engineering/actions/workflows/ci.yml/badge.svg)](https://github.com/ElaMCB/E2E-AI-engineering/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/coverage.json)
![Eval Score](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ElaMCB/E2E-AI-engineering/main/eval.json)
[![Maintained](https://img.shields.io/badge/Maintained-yes-success?style=flat-square)](https://github.com/ElaMCB/E2E-AI-engineering)

**Live portfolio:** https://elamcb.github.io/E2E-AI-engineering/

![Tech Stack](https://img.shields.io/badge/LangChain-OpenAI-orange?style=flat-square&logo=openai)
![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Tech Stack](https://img.shields.io/badge/Transformers-HuggingFace-yellow?style=flat-square&logo=huggingface)
![Tech Stack](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Tech Stack](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

This repo showcases end-to-end AI engineering with a focus on:

- **LLM-based agent architectures** (multi-agent, tools, RAG)
- **Evaluation and monitoring of agents** in realistic workflows
- **MLOps, data engineering, and automation** around these systems

It is designed to mirror responsibilities of Applied AI / LLM Agent Evaluation roles in production environments (e.g., healthcare, finance, operations).

## Projects

### Performance metrics

![Clinical Accuracy](https://img.shields.io/endpoint?url=https://elamcb.github.io/E2E-AI-engineering/badges/clinical.json)
![ICD-10 F1](https://img.shields.io/endpoint?url=https://elamcb.github.io/E2E-AI-engineering/badges/icd10.json)
![Cost per 1k](https://img.shields.io/endpoint?url=https://elamcb.github.io/E2E-AI-engineering/badges/cost.json)

**7-day F1 trend:** <img src="docs/assets/drift.svg" width="480" height="40" alt="7-day F1 trend">

| # | Project         | Last Update | Demo / Docs | Agent / Eval Focus |
|---|-----------------|-------------|-------------|---------------------|
| 1 | Excel/CSV Chat  | 2026-01-07 | [![Demo](https://img.shields.io/badge/Demo-Live-FF6B6B?style=flat-square)](https://huggingface.co/spaces/AzzuraM/excel-csv-chat-RAG) [![Blog](https://img.shields.io/badge/Blog-Read-blue?style=flat-square)](https://github.com/ElaMCB/E2E-AI-engineering/blob/main/ai-30day-sprint/p1-csv-chat/BLOG.md) | RAG pipeline, data eval, CSV/Excel QA |
| 2 | Tiny-LLM-LoRA   | 2026-01-07 | – | Fine-tuning + eval loops on small models |
| 3 | FinSent API     | 2026-01-05 | – | LLM API + regression tests on sentiment |
| 4 | GCP Pipeline    | 2026-01-05 | – | Data & training pipeline with CI/CD |
| 5 | AI Monitor      | 2026-01-07 | [![Dashboard](https://img.shields.io/badge/Dashboard-Live-9B59B6?style=flat-square)](https://elamcb.github.io/E2E-AI-engineering/intelligence.html) [![Architecture](https://img.shields.io/badge/Architecture-Docs-blue?style=flat-square)](https://github.com/ElaMCB/E2E-AI-engineering/blob/main/ai-monitor/AGENT_ARCHITECTURE.md) | Multi-agent monitor + eval of news quality |

Each project includes evaluation notes: see `EVAL_NOTES.md` in each project folder.

<details>
<summary><b>Evaluation internals</b> (click to expand)</summary>

See [evals/](evals/) for evaluation patterns, A/B testing frameworks, and case studies.

- [Evaluation Framework](evals/README.md) - High-throughput eval pipelines, A/B tests, and monitoring patterns
- [Healthcare Case Study](docs/canvas_agent_eval_case_study.md) - Healthcare agent evaluation example

**Implementation details:**
- 1k+ eval runs per PR, 12-model matrix, seeded RNG
- Gold labels expert-reviewed via structured workflow
- Drift-alert opens GitHub issue if F1 drops 2%+
</details>

---

## Additional Tools

| Tool | Status | Description |
|------|--------|-------------|
| [AI Monitor](ai-monitor/) | ![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square) | Weekly automated monitoring of AI market advances (DeepSeek, Kimi, etc.) |

---

![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ElaMCB/E2E-AI-engineering)

