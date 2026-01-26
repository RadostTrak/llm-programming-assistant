from state import DebuggingState
from assistants.triage_agent import triage_agent
from agents import Runner
import asyncio

# Initialize state
state = DebuggingState()

# Set prompt
prompt = 'I am having trouble with my code.'


async def main():
    input_prompt = prompt
    triage_result = await Runner.run(
        starting_agent=triage_agent, 
        input=[
            {"role": "user", "content": input_prompt}
        ],
        context={'state': state}
        )
    print("Triage Agent Result:", triage_result)
    print("Current State:", state)
    print("State:", state.diagnostic_findings)


asyncio.run(main())
