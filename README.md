# ⚖️ Lex-Agentic: Self-Correcting Legal Auditor

[![Stack](https://img.shields.io/badge/Stack-LangGraph%20%7C%20Qdrant%20%7C%20OpenAI-blue)](https://github.com/sudheerdunga/lex-agentic-auditor)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow)](https://www.python.org/)
[![Privacy](https://img.shields.io/badge/Privacy-Zero--Leakage-green)](#privacy--security)

**Lex-Agentic** is a production-grade AI agentic system for automating the review and audit of legal contracts. Built for the 2026 AI landscape, it prioritizes inference economics and data sovereignty by using a multi-agent, stateful graph architecture that supports self-correction and iterative research.

---

## 🏗️ System architecture

Unlike a linear RAG (retrieval-augmented generation) pipeline, Lex-Agentic uses a Stateful Cyclic Graph. If an audit step uncovers a discrepancy, the system can re-trigger research and re-evaluate findings before producing the final report.

### Key modules

- **Privacy Guard** (`redactor.py`) — Local NLP-based PII masking using Microsoft Presidio. Helps with compliance (e.g., India's DPDP Act, GDPR).
- **Vector Memory** (`research_storage.py`) — Local Qdrant vector database for fast retrieval of legal precedents and context.
- **Agentic Brain** (`agent_brain.py`) — LangGraph-managed workflow that coordinates nodes for redaction, research, and auditing.

---

## 🛠️ Technical stack

| Layer | Component | Notes |
|---|---|---|
| Orchestration | LangGraph | Stateful agent coordination, cyclic workflows |
| Memory | Qdrant | Local vector DB with hybrid search options |
| Embeddings | FastEmbed / BGE-Small-v1.5 | Efficient local embeddings (configurable) |
| Inference | GPT-4o-mini (or configured LLM) | Optimized for reasoning cost-efficiency |
| Privacy | Microsoft Presidio | Local PII anonymization/redaction |

---

## 🚀 Installation & usage

1. Clone the repository:

```bash
git clone https://github.com/sudheerdunga/lex-agentic-auditor.git
cd lex-agentic-auditor
```

2. Create and activate a virtual environment (macOS / Linux):

```bash
python -m venv venv
source venv/bin/activate
```

(On Windows PowerShell use: `./venv/Scripts/Activate.ps1`)

3. Install dependencies and language models:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

4. Configure secrets:

Create a `.env` file in the project root and add your API key:

```text
OPENAI_API_KEY=sk-xxxx...
# Other provider keys as needed
```

5. Run the auditor:

```bash
python agent_brain.py
```

## Privacy & security

This project enforces client-side redaction: any PII is anonymized locally by `redactor.py` before data leaves the host. Only anonymized legal context and logic are sent to remote inference engines (if configured). Review the code and environment settings before connecting external LLMs to ensure compliance with your data policies.

## Roadmap

- [ ] Multi-Agent Debate: add specialized "Prosecutor" and "Defense" agents to challenge findings.
- [ ] Local-Only Mode: integrate Llama 3.3 or other local models for air-gapped deployments.
- [ ] Streamlit UI: build a professional dashboard for lawyers to inspect graph state and audit results.

---

## Developer

- Sudheer Dunga — AI Solutions Architect
- Contact: sudheer.analytics@gmail.com
- Repo: https://github.com/sudheerdunga/lex-agentic-auditor

If you'd like, I can also:

- add a small `CONTRIBUTING.md` with developer setup tips
- add a quick self-check script to validate environment and secrets

