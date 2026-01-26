from agents import Agent, RunContextWrapper, function_tool

from state import DebuggingState

@function_tool
def update_triage_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Tool for the triage agent to record its findings.
    The agent will call this function when it has analyzed the issue.
    """
    state: DebuggingState = ctx.context["state"]
    state.diagnostic_findings['triage'] = finding
    state.current_phase = 'diagnosing'
    return f"Recorded finding: {finding}"

@function_tool
def get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the agent to read current state.
    The agent calls this to see what's been done so far.
    """
    state: DebuggingState = ctx.context["state"]
    return {
        'issue': state.issue_description,
        'previous_findings': state.diagnostic_findings,
        'attempted_solutions': state.attempted_solutions,
        'current_phase': state.current_phase
    }


TRIAGE_INSTRUCTIONS = (
    "You are a triage agent that speaks to a student facing an issue with their code "
    "and collects information for a diagnostic agent.\n\n"
    "IMPORTANT TOOLING RULES (follow these every turn):\n"
    "1) ALWAYS call get_debugging_context at the start of every turn.\n"
    "2) Ask a small set of brief, targeted questions.\n"
    "3) ALWAYS call update_triage_findings at the end of every turn.\n"
    "The finding must summarize what you know so far AND list what is still missing.\n\n"
    "If you have enough information for diagnosis, include a clear summary for the "
    "diagnostic agent in update_triage_findings and then hand off."
)


triage_agent = Agent(
    name="Triage Agent",
    model="gpt-5-nano",
    instructions=TRIAGE_INSTRUCTIONS,
    tools=[update_triage_findings, get_debugging_context],
    handoffs=[],
)