from assistants.triage_agent import triage_agent
from assistants.socratic_agent import socratic_agent
from agents import Agent, RunContextWrapper, function_tool
from utils.handoff import create_handoff_function
from utils.state_tools import get_debugging_context
from state import DebuggingState

@function_tool
def update_diagnostic_plan(ctx: RunContextWrapper[dict], plan: str):
    """
    Tool for the diagnostic agent to record its findings.
    """
    state: DebuggingState = ctx.context["state"]
    state.current_phase = 'diagnosing'
    state.diagnostic_plan = plan
    return f"Plan saved: {plan[:100]}..."


DIAGNOSTIC_INSTRUCTIONS = (
    "You are a diagnostic agent that diagnoses the student's issue and creates learning plans."

    "IMPORTANT TOOLING RULES (follow these every turn):\n"
    "1) ALWAYS call get_debugging_context at the START to see triage findings and any previous work.\n"
    "2) When you create a plan, ALWAYS call update_diagnostic_plan(plan='...') with numbered steps.\n"
    "   Example: update_diagnostic_plan(plan='Step 1: Ask what = does. Step 2: Ask what == does. Step 3: Guide to identify which is needed.')\n"
    "3) NEVER provide code or complete solutions.\n\n"

    "Decision tree:\n"
    "IF triage findings are insufficient (missing key info):\n"
    "  → Call transfer_to_triage(reason='Need more info on: [specific gaps]')\n\n"
    
    "IF triage findings are sufficient:\n"
    "  → Call update_diagnostic_plan() with your diagnosis and a step-by-step plan for helping the student understand how to resolve the issue\n"
    "  → Call transfer_to_socratic(reason='Diagnosis complete. Plan: [plan]')\n\n"
    
    "IF socratic hands back with feedback:\n"
    "  → Review their feedback in get_debugging_context()['socratic_feedback_history']\n"
    "  → Call update_diagnostic_plan() with REVISED plan addressing their feedback\n"
    "  → Call transfer_to_socratic(reason='Revised plan based on: [feedback summary]')\n\n"
    
    "IF you've revised the plan 3+ times OR socratic reports student frustration:\n"
    "  → Don't transfer. Instead, tell the student you'll escalate to a human instructor.\n"
    "  → The conversation will end here.\n\n"
    
    "Plan guidelines:\n"
    "- Use simple language, no jargon\n"
    "- Each step should be one question for socratic to ask\n"
    "- Focus on concept understanding\n"
    "- Build from student's current understanding"

)


diagnostic_agent = Agent(
    name='Diagnostic Agent',
    model='gpt-5-nano',
    instructions=DIAGNOSTIC_INSTRUCTIONS,
    tools=[
        get_debugging_context,
        update_diagnostic_findings,
        # Automatically record handoffs when called
        create_handoff_function('diagnostic', triage_agent),
        create_handoff_function('diagnostic', socratic_agent)
    ]
)
