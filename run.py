from agents import Runner
from assistants.triage import triage_agent
from assistants.diagnostic import diagnostic_agent
from assistants.socratic import socratic_agent
from state import SharedState

# Initialize runner and state
runner = Runner()
state = SharedState()

# Define handoffs
triage_agent.handoffs = [diagnostic_agent]
diagnostic_agent.handoffs = [triage_agent, socratic_agent]
socratic_agent.handoffs = [diagnostic_agent]

done = False
phase = "triage"

# Simple main loop
done = False
phase = "triage"

# Minimal run loop for multi-agent system

while not done:
    if phase == "triage":
        try:
            question = runner.run_sync(triage_agent, input=state)
            if hasattr(question, "final_output"):
                question = question.final_output
        except Exception:
            question = f"(stub) Triage Agent: {triage_agent.instructions[:300]}"

        answer = input(question + "\n> ")
        state.student_inputs.append(answer)

        # Move to diagnostic after collecting at least 1 input
        if len(state.student_inputs) >= 1:
            state.triage_complete = True
            phase = "diagnostic"

        state.print_state()

    elif phase == "diagnostic":
        try:
            result = runner.run_sync(diagnostic_agent, input=state)
            if hasattr(result, "final_output"):
                result = result.final_output
        except Exception:
            result = f"(stub) Diagnostic Agent: {diagnostic_agent.instructions[:300]}"

        if isinstance(result, str):
            state.diagnosis = state.diagnosis or result

        # Decide next phase
        phase = "triage" if state.need_more_info else "socratic"

        state.print_state()

    elif phase == "socratic":
        try:
            result = runner.run_sync(socratic_agent, input=state)
            if hasattr(result, "final_output"):
                result = result.final_output
        except Exception:
            result = f"(stub) Socratic Agent: {socratic_agent.instructions[:300]}"

        if isinstance(result, str):
            state.last_agent = "socratic"
            state.triage_summary = state.triage_summary or result

        # Guardrail: if stuck, escalate
        if state.socratic_stuck_count > 2:
            state.escalate = True
            phase = "diagnostic"
        else:
            done = True  # Finished

        state.print_state()


print("Session finished")
