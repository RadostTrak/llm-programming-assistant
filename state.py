from typing import List, Optional

class SharedState:
    def __init__(self):
        # User input
        self.student_inputs: List[str] = []

        # Triage outputs
        self.triage_summary: Optional[str] = None
        self.triage_complete: bool = False

        # Diagnostic outputs
        self.diagnosis: Optional[str] = None
        self.plan: Optional[List[str]] = None

        # Socratic tracking
        self.socratic_step: int = 0
        self.socratic_stuck_count: int = 0

        # Control and guardrails
        self.need_more_info: bool = False
        self.escalate: bool = False

        # Debug / traceability
        self.last_agent: Optional[str] = None

    # Optional: helper to print state nicely
    def __repr__(self):
        return (
            f"SharedState(student_inputs={self.student_inputs}, "
            f"triage_summary={self.triage_summary}, triage_complete={self.triage_complete}, "
            f"diagnosis={self.diagnosis}, plan={self.plan}, "
            f"socratic_step={self.socratic_step}, socratic_stuck_count={self.socratic_stuck_count}, "
            f"need_more_info={self.need_more_info}, escalate={self.escalate}, "
            f"last_agent={self.last_agent})"
        )

