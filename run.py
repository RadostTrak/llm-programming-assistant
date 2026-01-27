from state import DebuggingState
from assistants import triage_agent, diagnostic_agent
from agents import Runner
import asyncio

# Initialize state
state = DebuggingState()

loop = 0

while loop <= 2:
    async def main():
        input_prompt = input(f'Request {loop}\n> ')
        triage_result = await Runner.run(
        starting_agent=triage_agent, 
        input=[
            {"role": "user", "content": input_prompt}
        ],
        context={'state': state}
        )
        print("Next question:", triage_result.final_output)
        print("Triage Agent Result:", triage_result)
        print("Current State:", state)
    asyncio.run(main())
    loop += 1


print("Final State:", state)