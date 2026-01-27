from agents import function_tool, RunContextWrapper
from state import DebuggingState

@function_tool
def get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the agent to read current debugging state.
    """
    state: DebuggingState = ctx.context["state"]
    return {
        'issue': state.issue_description,
        'code_context': state.code_context,
        'previous_findings': state.diagnostic_findings,
        'attempted_solutions': state.attempted_solutions,
        'current_phase': state.current_phase,
        'handoff_history': state.handoff_history
    }