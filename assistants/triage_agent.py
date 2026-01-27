from assistants.diagnostic_agent import diagnostic_agent
from utils.handoff import create_handoff_function
from agents import Agent, RunContextWrapper, function_tool
from utils.state_tools import get_debugging_context
from state import DebuggingState

@function_tool
def update_triage_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Tool for the triage agent to record its findings.
    The agent will call this function when it has analyzed the issue.
    """
    state: DebuggingState = ctx.context["state"]
    state.diagnostic_findings['triage'] = finding
    state.current_phase = 'triaging'
    return f"Recorded finding: {finding}"


TRIAGE_INSTRUCTIONS = (
    "You are a triage agent that speaks to a student facing an issue with their code "
    "and collects information for a diagnostic agent.\n\n"
    "IMPORTANT TOOLING RULES (follow these every turn):\n"
    "1) ALWAYS call get_debugging_context at the start of every turn.\n"
    "2) Ask one brief, targeted question which is directly relevant to the student/'s input.\n"
    "3) ALWAYS call update_triage_findings at the end of every turn.\n"
    "4) NEVER provide code, do not give away solutions or debugging steps.\n\n"
    "The finding must summarize what you know so far AND list what is still missing.\n\n"
    "You are solely collecting information through short questions, do not attempt to diagnose the problem."
    # "If you have enough information for diagnosis, include a clear summary for the "
    # "diagnostic agent in update_triage_findings and then hand off."
    "ALWAYS hand off to diagnostic agent after you ask one question. "
    "When you hand off, call transfer_to_diagnostic(reason='') with a brief clear explanation. "
)


triage_agent = Agent(
    name="Triage Agent",
    model="gpt-5-nano",
    instructions=TRIAGE_INSTRUCTIONS,
    tools=[
        get_debugging_context,
        update_triage_findings,
        # Automatically record handoffs when called
        create_handoff_function("triage", diagnostic_agent)
    ]
)