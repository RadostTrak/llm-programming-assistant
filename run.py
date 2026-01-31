import json
import asyncio
import agents_setup
from state import DebuggingState
from assistants.triage_agent import triage_agent
from assistants.diagnostic_agent import diagnostic_agent
from agents import Runner
from utils.file_utils import load_exercise_from_yaml
from utils.file_utils import save_state_to_json



# Initialize state and load exercise description
state = DebuggingState()
state = load_exercise_from_yaml("problemset2.yaml", "1.1")

async def main():
    loop = 0
    while loop <= 3:
        input_prompt = input(f'Request {loop}\n> ')
        
        triage_result = await Runner.run(
            starting_agent=triage_agent, 
            input=[{"role": "user", "content": input_prompt}],
            context={'state': state}
        )

        print("Triage Agent Result:", triage_result)
        print("Current State:", state.triage_findings, state.handoff_history)
        loop += 1

asyncio.run(main())

save_state_to_json(state, 'testing_session.json')