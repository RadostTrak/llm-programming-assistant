from agents import function_tool, RunContextWrapper
from state import DebuggingState

@function_tool
def triage_get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the triage agent to read current debugging state.
    The triage agent has access to the exercise description,
    previous triage findings, and handoff history.
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

        'triage_findings': state.triage_findings,
        'current_turn': state.current_turn,
        'handoff_history': state.handoff_history
    }


@function_tool
def diagnostic_get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the diagnostic agent to read current debugging state.
    The diagnostic agent has access to everything.
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

        'triage_findings': state.triage_findings,
        'diagnostic_plan': state.diagnostic_plan,
        'socratic_findings': state.socratic_findings,
        'socratic_feedback': state.socratic_feedback_history,

        'current_phase': state.current_phase,
        'current_turn': state.current_turn,
        'handoff_history': state.handoff_history
    }


@function_tool
def socratic_get_debugging_context(ctx: RunContextWrapper[dict]):
    """
    Tool for the socratic agent to read current debugging state.
    The socratic agent has access to the diagnostic plan 
    and previous socratic findings and feedback. 
    """
    state: DebuggingState = ctx.context["state"]
    return {
        'diagnostic_plan': state.diagnostic_plan,
        'socratic_findings': state.socratic_findings,
        'socratic_feedback': state.socratic_feedback_history
    }