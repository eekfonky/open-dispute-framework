# Open Dispute Framework (ODF) ⚖️

> **A sovereign, test-driven, anti-hallucination framework to empower unrepresented workers in employment grievances, settlement negotiations, and tribunal claims.**

---

## 🏔️ The Mission

When workers face unfair treatment, toxic workplaces, or hostile settlement agreements, they face extreme institutional asymmetry. Employers have HR teams and retained employment lawyers; workers often have no representation and only access to commodity AI models that hallucinate law, garble arithmetic, and invent fake rights.

**Open Dispute Framework (ODF)** solves this by enforcing **deterministic mathematical gates**, **Stage 0 statutory grounding**, **evidentiary tiering**, and a **zero-dependency TDD test suite**. It guarantees that whether an employee is represented by Claude, Cursor, Codex, or a local model, the AI cannot drift into hallucinated citations or erroneous math.

---

## 🛡️ Core Architectural Invariants

| Layer | Guarantee | Tool / Invariant |
| :--- | :--- | :--- |
| **Arithmetic Integrity** | Hourly rates, hours, holiday pay, PILON, and package sums must mathematically reconcile to the exact penny. | `tools/verify_facts.py` |
| **Statutory Service Gate** | Prevents AI from asserting Ordinary Unfair Dismissal if continuous service is below qualifying thresholds (e.g. <24m in UK). Forces Day-1 protections. | `tools/rights_gate.py` |
| **Limitation Clocks** | Computes statutory filing fuses, conciliation windows, and reasonable settlement consideration periods deterministically. | `tools/limitation_calc.py` |
| **Dynamic Legal Grounding** | Gathers and verifies primary labour statutes, dispute bodies, and sector regulators dynamically for **any country/sector** worldwide. | `tools/gather_law.py` |
| **Evidentiary Tiering** | Segregates contemporaneous proof (T1), recollection (T2), employer claims (T3), and analysis (A). | `EVIDENTIARY_CONVENTIONS.md` |
| **Without-Prejudice Quarantine** | Strict quarantine (`without_prejudice/`) preventing settlement talks from contaminating open claims. | `without_prejudice/` |
| **Zero-Regex Privacy Linter** | Deterministic Luhn checksums and structural token analysis to prevent PII leaks. | `tools/verify_privacy.py` |

---

## 🚀 Getting Started

### 1. Interactive Onboarding Wizard
Run the setup wizard to initialise your case structure and ground truth data:
```bash
python3 setup.py
```
This prompts for:
* **Jurisdiction & Industry Sector** (e.g. `Scotland / Social Care`, `Nigeria / Nursing`, `Ontario / Tech`).
* **Continuous Start Date** & Trigger Dates.
* **Hourly Rate & Weekly Hours** (automatically generates `evidence/facts.json`).

### 2. Run the Deterministic Test Suite
ODF uses Python's standard library `unittest` with **zero external dependencies** (`pip` or `pytest` not required):
```bash
python3 run_tests.py
```

### 3. Verify Facts & Calculate Fuses
```bash
# Verify financial math
python3 tools/verify_facts.py

# Check statutory rights & service gates
python3 tools/rights_gate.py

# Calculate critical tribunal deadlines & ACAS fuses
python3 tools/limitation_calc.py

# Pre-commit privacy & leak check
python3 tools/verify_privacy.py
```

---

## 🤖 For Standalone Chatbots (Claude, ChatGPT, Gemini)

If you cannot run Python or Git, you can copy the self-contained prompt bundle in **`ODF_STANDALONE_PROMPT.md`** and paste it directly into any web AI chat to instantly enforce all ODF guardrails.

---

## 📁 Repository Layout

```
open-dispute-framework/
├── AGENTS.md                   # Strict execution rules for AI agents
├── EVIDENTIARY_CONVENTIONS.md  # 4-tier evidentiary standards & citation anchors
├── ODF_STANDALONE_PROMPT.md    # Copyable prompt bundle for web chatbots
├── run_tests.py                # Zero-dependency test runner
├── setup.py                    # Interactive case onboarding wizard
├── case/                       # Append-only case history & logs
│   └── log.md                  # Chronological dispute ledger
├── evidence/                   # Facts & documentary evidence
│   ├── facts.json              # Single source of financial & employment truth
│   └── schedule.md             # Exhibit index matrix ([E1], [E2]...)
├── jurisdictions/              # Dynamic legal grounding specifications
├── tactics/                    # Counter-playbooks against employer intimidation
│   └── counter_moves.md        # Calm responses to exploding deadlines & wage withholding
├── templates/                  # Standardised legal letters & briefs
│   ├── formal_grievance_letter.md
│   └── solicitor_briefing_pack.md
├── tests/                      # Invariant test suite
│   ├── test_arithmetic_invariants.py
│   ├── test_dynamic_statutory_verification.py
│   └── test_privacy_linter.py
├── tools/                      # Deterministic Python tools
│   ├── gather_law.py           # Stage 0 legal discovery engine
│   ├── limitation_calc.py      # Statutory deadline engine
│   ├── rights_gate.py          # Service qualification gate
│   ├── verify_facts.py         # Financial arithmetic verifier
│   └── verify_privacy.py       # PII & leak linter
└── without_prejudice/          # Quarantined settlement offers & s.111A talks
```

---

## 📜 License
Released under the **MIT License**. Free and open for workers, trade unions, legal advice clinics, and developers worldwide.
