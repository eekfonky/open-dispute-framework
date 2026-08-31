# Open Dispute Framework (ODF)
> Grounded, anti-hallucination legal grievance and workplace dispute architecture for sovereign AI agents.

## Overview
Open Dispute Framework provides an unrepresented employee with an airtight, verifiable case architecture. It enforces strict mathematical integrity on financial claims, prevents hallucinations through verifiable statutory grounding, redacts sensitive PII before Git commits, and manages limitation fuse countdowns for dispute bodies worldwide.

---

## Architecture Principles
1. **Single Source of Truth (`evidence/facts.json`)**: All dates, numbers, statutory caps, and hours are stored as structured arithmetic. No AI generates numbers from prose.
2. **Deterministic Verification (`tools/verify_facts.py`)**: Pre-commit validation blocks commits containing arithmetic errors, uncited figures, or broken dependency chains.
3. **Stage 0 Statutory Grounding (`tools/gather_law.py`)**: When given any jurisdiction (e.g. *Scotland, England, Nigeria, Canada, Australia*) and industry sector (e.g. *Care, Nursing, Tech, Education*), the AI autonomously discovers and verifies:
   - Primary Labour/Employment Statutes.
   - Prescribed Whistleblowing & Regulatory Bodies.
   - Statutory Limitation Fuses (Tribunal / Court deadlines).
   - Dispute Resolution Procedures.
4. **Append-Only Memory (`case/log.md`)**: A continuous chronological ledger ensuring stateless LLMs (Claude, GPT, local models) retain 100% case context across sessions without context drift.
5. **Pre-flight Privacy Linter (`tools/verify_privacy.py`)**: Automatic scanning and redaction of National Insurance numbers, SSNs, bank accounts, and sensitive health identifiers.

---

## Quickstart

### 1. Initialise the Framework
```bash
python setup.py
```

### 2. Run Verification Checks
```bash
python tools/verify_facts.py
python tools/verify_privacy.py
python tools/limitation_calc.py
```
