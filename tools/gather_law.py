#!/usr/bin/env python3
"""
gather_law.py
Stage 0 Dynamic Legal Grounding Engine.
Instructs the AI agent to systematically research, verify, and document the statutory framework
and dispute resolution bodies for ANY given jurisdiction and industry sector.
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
FACTS_FILE = ROOT_DIR / "evidence" / "facts.json"
JURISDICTIONS_DIR = ROOT_DIR / "jurisdictions"

RESEARCH_PROMPT_TEMPLATE = """# Dynamic Legal Grounding Protocol: {jurisdiction} ({sector})

You are tasked with populating the statutory baseline for:
* **Jurisdiction / Region:** {jurisdiction}
* **Industry Sector:** {sector}

You MUST research, verify from official primary sources, and write a structured summary to:
`jurisdictions/{filename}.md`

## Mandatory Verification Checks (Zero Hallucination Standard)
1. **Primary Labour / Employment Statute:**
   - What is the exact title and enactment year of the primary employment act?
   - What sections govern unfair dismissal, constructive dismissal, and statutory notice?
2. **Whistleblowing & Regulatory Protections:**
   - What are the protected disclosure provisions?
   - What are the official Prescribed Persons / Regulators for {sector}?
3. **Statutory Dispute Resolution Body:**
   - What is the specific tribunal, industrial court, or arbitration commission?
   - Is pre-action conciliation or mediation mandatory?
4. **Limitation Fuses (Critical Deadlines):**
   - What is the exact statutory time limit to lodge a claim (e.g. 3 months, 6 months, 1 year)?
   - When does the clock start?
5. **Settlement / Severance Agreement Requirements:**
   - Does a binding exit agreement require independent legal certification?
"""

def generate_spec():
    if not FACTS_FILE.exists():
        print("[-] Error: evidence/facts.json not found. Run setup.py first.")
        sys.exit(1)

    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    jurisdiction = data.get("jurisdiction", {}).get("name", "Unknown")
    sector = data.get("jurisdiction", {}).get("sector", "General")
    
    clean_j = jurisdiction.lower().replace(" ", "_").replace("&", "and")
    clean_s = sector.lower().replace(" ", "_").replace("/", "_")
    filename = f"{clean_j}_{clean_s}"

    JURISDICTIONS_DIR.mkdir(exist_ok=True)
    prompt_file = JURISDICTIONS_DIR / f"RESEARCH_TASK_{filename}.md"
    
    content = RESEARCH_PROMPT_TEMPLATE.format(
        jurisdiction=jurisdiction,
        sector=sector,
        filename=filename
    )
    
    prompt_file.write_text(content, encoding="utf-8")
    print(f"[+] Generated dynamic research brief: {prompt_file.relative_to(ROOT_DIR)}")
    print(f"[+] The AI agent can now execute this research task and produce jurisdictions/{filename}.md")

if __name__ == "__main__":
    generate_spec()
