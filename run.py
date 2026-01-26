from assistants.triage import triage_agent
from assistants.diagnostic import diagnostic_agent
from assistants.socratic import socratic_agent
from state import SharedState

# Define handoffs
triage_agent.handoffs = [diagnostic_agent]
diagnostic_agent.handoffs = [triage_agent, socratic_agent]
socratic_agent.handoffs = [diagnostic_agent]

# Initialize shared state
state = SharedState()

# Function to print current state for debugging
def print_state(state):
    print("---- STATE ----")
    for field, value in state.__dict__.items():
        print(f"{field}: {value}")
    print("----------------\n")

done = False
phase = "triage"

# Main loop
while not done:
    if phase == "triage":
        question = triage_agent.run(state)
        answer = input(question + "\n> ")
        state.student_inputs.append(answer)

        # Decide if triage has enough info
        if len(state.student_inputs) >= 1:  # Simplest rule for now
            state.triage_complete = True
            phase = "diagnostic"

        print_state(state)  # Print after triage step

    elif phase == "diagnostic":
        diagnostic_agent.run(state)  # Fill state.diagnosis and state.plan

        if state.need_more_info:
            phase = "triage"
        else:
            phase = "socratic"

        print_state(state)  # Print after diagnostic step

    elif phase == "socratic":
        socratic_agent.run(state)  # Executes step-by-step plan

        if state.socratic_stuck_count > 1:  # Example stuck guardrail
            state.escalate = True
            phase = "diagnostic"
        else:
            done = True  # Student problem solved

        print_state(state)  # Print after socratic step
