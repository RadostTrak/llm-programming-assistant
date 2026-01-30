import json
from state import DebuggingState
from assistants.triage_agent import triage_agent
from assistants.diagnostic_agent import diagnostic_agent
from agents import Runner
import asyncio
import agents_setup

# Initialize state
state = DebuggingState()

async def main():
    loop = 0
    while loop <= 1:
        input_prompt = input(f'Request {loop}\n> ')
        
        triage_result = await Runner.run(
            starting_agent=triage_agent, 
            input=[{"role": "user", "content": input_prompt}],
            context={'state': state}
        )

        print("Triage Agent Result:", triage_result)
        print("Current State:", state)
        loop += 1

asyncio.run(main())

state.save_to_json('testing_session.json')