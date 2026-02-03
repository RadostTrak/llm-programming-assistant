from agents import Agent, RunContextWrapper, function_tool, ModelSettings
from utils.state_tools import triage_get_debugging_context
from assistants import diagnostic_agent
from utils.guardrails import code_detection_guardrail
from state import DebuggingState

@function_tool
def update_triage_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Tool for the triage agent to record its findings.
    The agent will call this function when it has analyzed the issue.
    """
    state: DebuggingState = ctx.context["state"]
    state.triage_findings.append(finding)
    state.current_phase = 'triaging'
    state.current_turn += 1
    return "Finding recorded."


TRIAGE_INSTRUCTIONS = (
    "You collect info about a student's Python problem, then hand off to diagnostic.\n"
    "You speak directly to the student. Your output should be a simple question a student can answer.\n"
    "GOAL: Learn WHAT they tried and WHAT went wrong. Not WHY or HOW to fix.\n\n"
    
    "PROCESS (follow every turn):\n"
    "1. ALWAYS triage_get_debugging_context() at the START of every turn to see what you already know.\n"
    "2. Then, ALWAYS call update_triage_findings(finding='...') to record a brief summary of the information you collected:\n"
    "   - Format: 'Turn X: [new info learned this turn]\n"
    "   - Example: 'Turn 2: Student tried input(width), got NameError about width being undefined'\n"
    "DO NOT include anything in the exercise description in the finding.\n"
    "3. Check transfer criteria:\n"
    "   a. Do you have code/description AND error/unexpected behavior? → transfer\n"
    "   b. Is the turn >= 4? → transfer\n"
    "4. If transfer:\n"
    "   a. CALL transfer_to_diagnostic(reason='[what you learned]')\n"
    "   b. Hand off to diagnostic_agent to transfer control\n"
    "   c. Do NOT generate any text response\n"
    "5. Otherwise: ask ONE question about what's missing (code OR error)\n\n"

    "Rules:\n"
    "- The student already has the exercise description. Do not repeat or summarise it.\n" 
    "- Ask exactly ONE question per turn. Do not ask compound questions with 'and' or commas.\n"
    "- Your question must respond directly to what the student just said. \n"
    "- Never provide code, solutions, or debugging steps.\n"
    "- Do not ask leading questions that reveal the solution structure.\n"
    "- Do not ask the student to explain the whole problem back to you.\n"
    "- Do not collect full tracebacks, line numbers, or environment details.\n"
    "- Focus on understanding: what they've tried, what happened, what they expected, or what they're confused about.\n\n"
    "- Do not include preambles, explanations, or meta-commentary. Output only your question.\n\n"
    
    "IF DIAGNOSTIC HANDS BACK:\n"
    "Diagnostic will tell you what is missing. Ask the student 1-2 focused questions to fill the gap, then transfer back immediately: "
    "Example: Diagnostic says 'need error message' → You ask: 'What error did you get?'\n"
    "Then transfer back immediately after student responds.:\n"
    "   a. CALL transfer_to_diagnostic(reason='[what you learned]')\n"
    "   b. Hand off to diagnostic_agent to transfer control\n"
    "   c. Do NOT generate any text response\n"
)


triage_agent = Agent(
    name="triage",
    model="gpt-5-mini",
    instructions=TRIAGE_INSTRUCTIONS,
    tools=[
        triage_get_debugging_context,
        update_triage_findings
    ],
    model_settings=ModelSettings(tool_choice='required'),
    handoffs=[],
    output_guardrails=[code_detection_guardrail]
)