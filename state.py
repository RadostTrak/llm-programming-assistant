class SharedState:
    def __init__(self):
        # User input
        self.student_inputs = []

        # Triage outputs
        self.triage_summary = None
        self.triage_complete = False

        # Diagnostic outputs
        self.diagnosis = None
        self.plan = []

        # Socratic tracking
        self.socratic_step = 0
        self.socratic_stuck_count = 0

        # Control and guardrails
        self.need_more_info = False
        self.escalate = False

        # Debug / traceability
        self.last_agent = None

    # Helper to print state nicely
    def print_state(self):
        print("---- SHARED STATE ----")
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")
        print("----------------------\n")