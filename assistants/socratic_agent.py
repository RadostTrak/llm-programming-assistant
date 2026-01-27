from agents import Agent, RunContextWrapper, function_tool
from utils.handoff import create_handoff_function
from utils.state_tools import get_debugging_context
from state import DebuggingState


@function_tool
def update_socratic_findings(ctx: RunContextWrapper[dict], question: str, response: str, outcome: str):
    """
    Socratic agent to records each interaction with student.
    """
    state: DebuggingState = ctx.context["state"]
    state.current_phase = 'questioning'
    state.socratic_attempted_solutions.append({
        'question': question,
        'response': response,
        'outcome': outcome
    })
    return f"Attempt recorded. Total: {len(state.socratic_attempted_solutions)}"


@function_tool
def add_feedback_for_diagnostic(ctx: RunContextWrapper[dict], feedback: str):
    """Socratic gives feedback when handing back to diagnostic"""
    state: DebuggingState = ctx.context["state"]
    state.socratic_feedback_history.append(feedback)
    return f"Feedback recorded"


SOCRATIC_INSTRUCTIONS = (
    "You are a Socratic agent that helps students learn through guided questioning. "

    "IMPORTANT TOOLING RULES (follow these EVERY turn):\n"
    "1) ALWAYS call get_debugging_context() at the START to see the diagnostic plan and student progress.\n"
    "2) After student responds, ALWAYS call record_socratic_attempt(question='...', student_response='...', outcome='...') to track progress.\n"
    "3) If handing back to diagnostic, ALWAYS call socratic_feedback_history(feedback='...') first.\n"
    "4) NEVER write code or give direct solutions.\n\n"

    "Your process:\n"
    "- Execute diagnostic agent's plan one step at a time through a Socratic questioning method\n"
    "- Record the student's attempt and whether they understood\n"
    "- If they understand, move to next step\n"
    "- Guide with theoretical explanations if stuck\n"
    "- If they don't understand after 2-3 attempts on same question, note this\n\n"
    
    "When to hand back to diagnostic:\n"
    "IF you're stuck in loops (asking same concept 3+ times with no progress):\n"
    "  → Call socratic_feedback_history(feedback='Looping on [concept]. Student responses: [summary].')\n"
    "  → Call transfer_to_diagnostic(reason='Plan not effective, provided feedback')\n\n"
    
    "IF student shows signs of frustration:\n"
    "  → Call socratic_feedback_history(feedback='Student frustrated. Quote: [their words]. May need simpler approach or different angle.')\n"
    "  → Call transfer_to_diagnostic(reason='Student showing frustration')\n\n"    
)


socratic_agent = Agent(
    name='Socratic Agent',
    # give feedback for diagnostic agent when handing off
    model='gpt-5-nano',
    instructions=SOCRATIC_INSTRUCTIONS,
    tools=[
        get_debugging_context,
        update_socratic_findings,
        add_feedback_for_diagnostic
    ]
)
