from assistants import triage_agent, diagnostic_agent, socratic_agent
from utils.handoff import create_record_handoff_function

# Add handoffs to triage agent
triage_agent.tools.append(
    create_record_handoff_function('triage', diagnostic_agent)
)
triage_agent.handoffs = [diagnostic_agent]

# Add handoffs to diagnostic agent
diagnostic_agent.tools.extend([
    create_record_handoff_function('diagnostic', triage_agent),
    create_record_handoff_function('diagnostic', socratic_agent)
])
diagnostic_agent.handoffs = [triage_agent, socratic_agent]

# Add handoffs to socratic agent
socratic_agent.tools.append(
    create_record_handoff_function('socratic', diagnostic_agent)
)
socratic_agent.handoffs = [diagnostic_agent]