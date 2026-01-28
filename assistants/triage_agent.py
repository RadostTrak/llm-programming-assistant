from agents import Agent, RunContextWrapper, function_tool
from utils.handoff import create_handoff_function
from utils.state_tools import triage_get_debugging_context
from state import DebuggingState

@function_tool
def update_triage_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Tool for the triage agent to record its findings.
    The agent will call this function when it has analyzed the issue.
    """
    state: DebuggingState = ctx.context["state"]
    state.triage_findings = finding
    state.current_phase = 'triaging'
    return f"Recorded finding: {finding}"


TRIAGE_INSTRUCTIONS = (
    "You are a triage agent that speaks to a student facing an issue with their code "
    "and collects information for a diagnostic agent.\n\n"
    "IMPORTANT TOOLING RULES (follow these every turn):\n"
    "1) ALWAYS call triage_get_debugging_context() at the START of every turn to see what you already know.\n"
    "2) ALWAYS call update_triage_findings(finding='...') at the END of every turn with a summary of:\n"
    "   - What information you've collected so far\n"
    "   - What is still missing or unclear\n"
    "3) NEVER provide code, solutions, or debugging steps.\n\n"
    "Ask ONE brief, targeted question which is directly relevant to the student's input and what is missing. "
    "After the student responds, update your findings with what you learned. "
    "The finding must summarize what you know so far AND list what is still missing.\n\n"
    "After a maximum of 2 questions or when you have enough information, "
    "call transfer_to_diagnostic(reason='Collected: [brief summary]. Ready for diagnosis.'). "
    "You are solely collecting information through short questions, do not attempt to diagnose the problem."
)


triage_agent = Agent(
    name="Triage Agent",
    model="gpt-5-nano",
    instructions=TRIAGE_INSTRUCTIONS,
    tools=[
        triage_get_debugging_context,
        update_triage_findings
    ]
)