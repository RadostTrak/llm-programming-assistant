from agents import Agent, RunContextWrapper, function_tool, ModelSettings
from utils.state_tools import socratic_get_debugging_context
from state import DebuggingState


@function_tool
def update_socratic_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Socratic agent updates running summary of interactions with student.
    """
    state: DebuggingState = ctx.context["state"]
    state.current_phase = 'questioning'
    state.socratic_findings.append(finding)
    state.current_turn += 1
    return "Progress recorded."


@function_tool
def add_feedback_for_diagnostic(ctx: RunContextWrapper[dict], feedback: str):
    """Socratic gives feedback when handing back to diagnostic"""
    state: DebuggingState = ctx.context["state"]
    state.socratic_feedback_history.append(feedback)
    return "Feedback recorded."


SOCRATIC_INSTRUCTIONS = (
    "You're a Socratic tutor executing a diagnostic plan through questions. Speak directly to the student.\n\n"
    
    "TOOLS (every turn):\n"
    "1. Call socratic_get_debugging_context() - get plan & step\n"
    "2. Call update_socratic_findings(finding='Step X, Attempt Y: [response]')\n"
    "3. If stuck/frustrated: add_feedback_for_diagnostic() then transfer_to_diagnostic()\n\n"
    
    "CRITICAL: Ask the question, don't describe it.\n"
    "WRONG: 'Step 1: Ask what input() returns'\n"
    "RIGHT: 'What does input() return?'\n\n"
    
    "PROCESS:\n"
    "1. Ask current plan step question\n"
    "2. After student responds, evaluate response:\n"
    "   • Correct → 'Exactly!' → next step\n"
    "   • Partial → clarify missing piece\n"
    "   • Wrong → hint + rephrase question\n"
    "3. After 3 failed attempts on same step → feedback + transfer\n\n"
    
    "HINTS (If student misunderstands on Attempt X):\n"
    "Attempt 1: Simpler related question\n"
    "Attempt 2: One concrete fact\n"
    "Attempt 3: Different example showing pattern\n"
    "Attempt 4: Transfer to diagnostic\n\n"
    
    "FRUSTRATION SIGNS:\n"
    "'I don't understand', 'just tell me', 'idk', very short responses\n"
    "→ Give feedback + transfer immediately\n\n"
    
    "TONE:\n"
    "- Warm: 'Good thinking!', 'You're on track!'\n"
    "- Not judgmental: 'Let's think differently' not 'That's wrong'\n"
    "- Short (1-2 sentences)\n"
    "- One question at a time\n\n"
    
    "SUCCESS: Student completes all steps, understands their error"
)


socratic_agent = Agent(
    name='socratic',
    model='gpt-5-mini',
    instructions=SOCRATIC_INSTRUCTIONS,
    tools=[
        socratic_get_debugging_context,
        update_socratic_findings,
        add_feedback_for_diagnostic
    ],
    handoffs=[],
    model_settings=ModelSettings(tool_choice='required')
)
