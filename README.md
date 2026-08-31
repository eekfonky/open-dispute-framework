# Open Dispute Framework (ODF) ⚖️

> **A sovereign, test-driven, and anti-hallucination framework designed to empower unrepresented workers in workplace disputes, grievances, and settlement negotiations.**

---

## 🌟 The Mission

Workplace disputes are among the most stressful events in a person's life. When an employee faces unfair treatment, constructive dismissal, or a sudden settlement agreement, the playing field is heavily tilted: employers have dedicated HR departments, retained solicitors, and institutional leverage, while the worker is often left alone.

General-purpose AI can help, but commodity chatbots come with dangerous risks: they hallucinate laws from the wrong countries, invent non-existent statutory rights, and garble financial arithmetic.

**Open Dispute Framework (ODF)** is an open-source, mathematically grounded toolkit that turns any AI agent (Claude Code, Cursor, Codex, ChatGPT, or local models) into a precise, disciplined legal research and evidentiary compilation assistant. It replaces guesswork with **deterministic verification gates**, **service qualification checks**, **evidentiary tiering**, and **zero-dependency test suites**.

---

## 🎬 What to Expect on Your First Run

Whether you run ODF via the interactive Python wizard or open this repository with an AI coding assistant (like Claude Code, Cursor, or Codex), here is what the onboarding process looks like from start to finish:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GATHER DOCUMENTS ──► Contract, Payslips, Policies, Proof  │
│                                                             │
│ 2. STEP 0 INTAKE     ──► AI asks 5 core questions            │
│                                                             │
│ 3. GROUND TRUTH LOCK ──► Math & Service thresholds verified  │
│                                                             │
│ 4. STATUTORY ROOT   ──► Real laws fetched (zero hallucination)│
│                                                             │
│ 5. ACTIONABLE PACK   ──► Grievance letters & lawyer briefs   │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Gather Your Foundational Documents
Before you start, collect whatever documents you have and place them in the project folders:
* 📄 **`evidence/documents/`**:
  * **Employment Contract / Statement of Terms** *(to check notice periods, hours, pay)*.
  * **Recent Payslips (Last 3 Months)** *(to lock in gross pay and hourly rate)*.
  * **Workplace Policies** *(Grievance, Disciplinary, Sickness/Absence policies)*.
  * **Contemporaneous Evidence** *(emails, text messages, notes, GP fit notes)*.
* 🔒 **`without_prejudice/`**:
  * Any draft settlement agreements, severance offers, or letters marked *"Without Prejudice"* or *"s.111A Pre-termination Negotiations"*.

### Step 2: The Initial Intake Questions
When you run `python3 setup.py` (or when your AI agent reads `AGENTS.md`), you will be guided through 5 simple questions:
1. **Where do you work?** (e.g. *Scotland, England & Wales, Ontario, Nigeria*) — sets the legal jurisdiction.
2. **What industry/sector?** (e.g. *Care/Nursing, Tech, Hospitality, Office Admin*) — discovers sector-specific regulators.
3. **When did you start?** (Continuous start date) — calculates continuous service months.
4. **What is your current status?** (e.g. *Employed, suspended on full pay, under investigation, dismissed, or offered a settlement*).
5. **What was the trigger event?** (e.g. *Unresolved bullying grievance, sudden disciplinary invite, or received a settlement proposal*).

### Step 3: The Ground Truth Lock
The framework writes your information to **`evidence/facts.json`** and runs automated checks:
* **Service Qualifying Gate:** Calculates whether you have the service length for ordinary unfair dismissal (e.g. 2 years in the UK). If not, it automatically locks the AI onto **Day-1 statutory protections** (Whistleblowing, Equality Act / Discrimination, Health & Safety, Unlawful Wage Deductions).
* **Penny-Exact Arithmetic:** Verifies that your hourly rate, contracted hours, holiday pay balance, notice pay (PILON), and ex-gratia sums balance exactly to the penny.

### Step 4: Live Case Building & Strategy
Once initialised, you and your AI agent can safely:
* Build an immutable, date-stamped chronology in **`case/log.md`**.
* Classify evidence into reliable tiers (**T1** Contemporaneous, **T2** Recollection, **T3** Employer claim, **A** Analysis) via **`EVIDENTIARY_CONVENTIONS.md`**.
* Calculate ACAS and tribunal limitation fuses via **`tools/limitation_calc.py`**.
* Draft calm, assertive **Formal Grievance Letters** or **Solicitor Briefing Packs** using the templates in **`templates/`**.

---

## 🚀 How to Use It

### Option A: Interactive Onboarding (Python / Terminal)
If you have a terminal or code editor:

1. **Initialise your case:**
   ```bash
   python3 setup.py
   ```
2. **Run the Invariant Test Suite:**
   ```bash
   python3 run_tests.py
   ```
   *(Uses Python's standard library `unittest` — zero `pip` or external dependencies required).*

3. **Verify Facts & Deadlines:**
   ```bash
   python3 tools/verify_facts.py      # Verifies financial arithmetic
   python3 tools/rights_gate.py       # Validates service qualifying periods
   python3 tools/limitation_calc.py   # Computes critical tribunal fuses
   python3 tools/verify_privacy.py    # Pre-commit privacy & leak check
   ```

---

### Option B: Autonomous AI Agents (Claude Code, Cursor, Codex, Hermes)
If you open this repository in an AI-powered coding tool:
* The agent automatically reads **`AGENTS.md`**.
* If `evidence/facts.json` is not yet populated, the agent will **automatically welcome you, ask the 5 initial setup questions**, and extract numbers from your uploaded contracts and payslips.

---

### Option C: Standalone Web Chatbot (No Installation Needed)
If you do not have Python or Git, you can use ODF inside **Claude, ChatGPT, or Gemini**:

1. Open **`ODF_STANDALONE_PROMPT.md`**.
2. Copy the prompt block and paste it into your AI chat.
3. The AI will immediately enforce all ODF arithmetic rules, statutory service gates, and anti-hallucination boundaries.

---

## 🛡️ Core Guarantees & Features

* 🧮 **Exact Financial Arithmetic:** All holiday pay, notice pay (PILON), monthly gross wages, and ex-gratia sums must balance to the penny via `tools/verify_facts.py`.
* ⏱️ **Limitation Fuse Clocks:** Deterministically computes statutory deadlines (e.g. ACAS 3-month Early Conciliation limits in the UK, the 10-day settlement consideration window, and whistleblowing interim relief fuses).
* 🚪 **Statutory Service Gates:** Calculates continuous employment service to prevent the AI from asserting rights requiring qualifying service (e.g. 2-year unfair dismissal in the UK), automatically forcing the agent to focus on Day-1 statutory protections (Whistleblowing Detriment, Equality Act / Discrimination, Health & Safety, and Unlawful Wage Deductions).
* 🌍 **Dynamic Legal Ingestion (Worldwide):** Gathers and verifies primary labour statutes, dispute bodies, and sector regulators dynamically for **any country or region** across the globe without hardcoded regional bias.
* 📑 **4-Tier Evidentiary Classification:** Strictly separates contemporaneous proof (T1), recollection (T2), employer assertions (T3), and legal analysis (A).
* 🔒 **Without-Prejudice Quarantine:** Quarantines protected settlement discussions (`without_prejudice/`) to prevent them from contaminating open grievance letters or tribunal claim drafts.
* 🛡️ **Zero-Regex Privacy Verification:** Uses deterministic Luhn checksums and structural token analysis to prevent accidental leaks of National Insurance numbers, bank details, and payment cards.

---

## 📁 Repository Structure

```
open-dispute-framework/
├── AGENTS.md                   # Universal execution rules for AI agents
├── EVIDENTIARY_CONVENTIONS.md  # 4-tier evidentiary standards & citation anchors
├── ODF_STANDALONE_PROMPT.md    # Copyable prompt bundle for web chatbots
├── run_tests.py                # Zero-dependency test runner
├── setup.py                    # Interactive case onboarding wizard
├── case/                       # Append-only case history & logs
│   └── log.md                  # Chronological dispute ledger
├── evidence/                   # Facts & documentary evidence
│   ├── documents/              # Place contracts, policies, payslips, emails here
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

## ⚖️ Legal Disclaimer

> **IMPORTANT:** The Open Dispute Framework (ODF) is an open-source software and research tool designed to help workers organize evidence, verify mathematics, and compile case materials. 
>
> **ODF does not provide formal legal advice, establish an attorney-client relationship, or guarantee legal outcomes.** Employment laws, tribunal rules, and limitation periods vary across jurisdictions and change over time. 
>
> Users should always have their case, correspondence, and settlement agreements reviewed by a qualified employment solicitor, certified trade union representative, or authorized legal advice clinic (such as ACAS, Citizens Advice, or local Law Centres) before taking binding legal actions or signing agreements.

---

## 📜 License & Community

Released under the **MIT License**. Free to use, adapt, and distribute for workers, trade unions, legal advice clinics, and software developers worldwide.
