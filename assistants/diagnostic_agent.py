from agents import Agent, RunContextWrapper, function_tool
from state import DebuggingState

@function_tool
def update_diagnostic_findings(ctx: RunContextWrapper[dict], finding: str):
    """
    Tool for the diagnostic agent to record its findings.
    """
    state: DebuggingState = ctx.context["state"]
    state.diagnostic_findings['diagnostic'] = finding
    state.current_phase = 'diagnosing'
    return f"Recorded finding: {finding}"


diagnostic_agent = Agent(
    name='Diagnostic Agent',
    model='gpt-5-nano',
    instructions=(
        'You are a diagnostic agent.'
        'You will receive information from the triage agent about the student\'s issue.'
        
        # socratic handoff
        'If you have received sufficient information from the triage agent to make a diagnosis, then diagnose the problem, '
        'then make a step-by-step plan of how to resolve the student\'s problem. '
        'The plan should focus on student understanding, and explain concepts in simple terms when needed.'
        'Do not use jargon nor assume prior knowledge, and do not use any language constructs beyond '
        'basic syntax, ' # unless explicitly stated in the exercise or context.
        'Encourage students to think through problems and guide them with questions, rather than giving direct answers. '
        'Do not ever write any code or suggest complete code solutions; instead, help students debug and understand their own code through theoretical explanations. '
        'Finally, hand off the plan to socratic agent.'
        
        # triage handoff
        'If you have not received sufficient information from the triage agent to be able to diagnose the problem, then hand back to the triage agent to collect more information.'
        
        # socratic hand back
        'If socratic agent hands back to you, then revise the plan you made based on the feedback from socratic agent, and finally hand back to socratic agent.'

        # escalation
        'You may choose to escalate and end the conversation if socratic agent hands back to you multiple times,'
        'or if you are unable to diagnose the problem or make a good plan and ask the triage agent for more information multiple times.'
        'If socratic agent reports signs of frustration from the student, escalate and end the conversation politely.'
    ),
    handoffs=[]
)
