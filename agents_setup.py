from assistants import triage_agent, diagnostic_agent, socratic_agent
from utils.handoff import create_handoff_function

# Add handoffs to triage agent
triage_agent.tools.append(
    create_handoff_function('triage', diagnostic_agent)
)

# Add handoffs to diagnostic agent
diagnostic_agent.tools.extend([
    create_handoff_function('diagnostic', triage_agent),
    create_handoff_function('diagnostic', socratic_agent)
])

# Add handoffs to socratic agent
socratic_agent.tools.append(
    create_handoff_function('socratic', diagnostic_agent)
)