from pydantic import BaseModel
from typing import List, Optional

class SharedState(BaseModel):
    # User input
    student_inputs: List[str] = []

    # Triage outputs
    triage_summary: Optional[str] = None
    triage_complete: bool = False

    # Diagnostic outputs
    diagnosis: Optional[str] = None
    plan: Optional[List[str]] = None

    # Socratic tracking
    socratic_step: int = 0
    socratic_stuck_count: int = 0

    # Control and guardrails
    need_more_info: bool = False
    escalate: bool = False

    # Debug / traceability
    last_agent: Optional[str] = None

    # Helper to print state nicely
    def print_state(self):
        print("---- SHARED STATE ----")
        for field, value in self.dict().items():
            print(f"{field}: {value}")
        print("----------------------\n")
