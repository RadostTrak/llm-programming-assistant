from agents import function_tool, RunContextWrapper
from state import DebuggingState

@function_tool
def get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the agent to read current debugging state.
    """
    state: DebuggingState = ctx.context["state"]
    return {
        'exercise': {
            'broad_context': state.broad_context,
            'id': state.exercise_id,
            'title': state.exercise_title,
            'prompt': state.exercise_prompt,
            'context': state.exercise_context
        },

        # Agent work
        'triage_findings': state.triage_findings,
        'diagnostic_plan': state.diagnostic_plan,
        'socratic_findings': state.socratic_findings,
        'socratic_feedback': state.socratic_feedback_history,

        # Progress
        'current_phase': state.current_phase,
        'handoff_history': state.handoff_history,
    }