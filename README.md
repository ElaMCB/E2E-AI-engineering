# E2E-AI-engineering

Live portfolio: https://elamcb.github.io/E2E-AI-engineering/

## Why this repo exists

This repo showcases end-to-end AI engineering with a focus on:

- **LLM-based agent architectures** (multi-agent, tools, RAG)
- **Evaluation and monitoring of agents** in realistic workflows
- **MLOps, data engineering, and automation** around these systems

It is designed to mirror responsibilities of Applied AI / LLM Agent Evaluation roles in production environments (e.g., healthcare, finance, operations).

---

## Projects

| # | Project         | Status  | Demo / Docs | Agent / Eval Focus |
|---|-----------------|---------|-------------|---------------------|
| 1 | Excel/CSV Chat  | Done | [Live Demo](https://huggingface.co/spaces/AzzuraM/excel-csv-chat-RAG) / [Blog](https://github.com/ElaMCB/E2E-AI-engineering/blob/main/ai-30day-sprint/p1-csv-chat/BLOG.md) | RAG pipeline, data eval, CSV/Excel QA |
| 2 | Tiny-LLM-LoRA   | WIP  | –          | Fine-tuning + eval loops on small models |
| 3 | FinSent API     | Todo | –          | LLM API + regression tests on sentiment |
| 4 | GCP Pipeline    | Todo | –          | Data & training pipeline with CI/CD |
| 5 | AI Monitor      | Done | [Intelligence Dashboard](https://elamcb.github.io/E2E-AI-engineering/intelligence.html) / [Architecture](https://github.com/ElaMCB/E2E-AI-engineering/blob/main/ai-monitor/AGENT_ARCHITECTURE.md) | Multi-agent monitor + eval of news quality |

Each project includes evaluation notes: see `EVAL_NOTES.md` in each project folder.

## Agent Evaluation

See [evals/](evals/) for evaluation patterns, A/B testing frameworks, and Canvas-style case studies.

- [Evaluation Framework](evals/README.md) - High-throughput eval pipelines, A/B tests, and monitoring patterns
- [Canvas-style Case Study](docs/canvas_agent_eval_case_study.md) - Healthcare agent evaluation example

---

## Additional Tools

| Tool | Description |
|------|-------------|
| [AI Monitor](ai-monitor/) | Weekly automated monitoring of AI market advances (DeepSeek, Kimi, etc.) |

---

Visitor badge (auto-updated)  
![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ElaMCB/E2E-AI-engineering)

