import json
import asyncio
import agents_setup
from state import DebuggingState
from assistants import triage_agent, diagnostic_agent, socratic_agent
from agents import Runner
from utils.file_utils import load_exercise_from_yaml
from utils.file_utils import save_state_to_json

# Initialize state and load exercise description
state = DebuggingState()
state = load_exercise_from_yaml("problemset2.yaml", "1.1")

# Track which agent is currently active
current_agent = triage_agent


async def main():
    global current_agent

    loop = 1
    while loop <= 8:
        input_prompt = input(f'Request {loop}\n> ')
        
        result = await Runner.run(
            starting_agent=current_agent, 
            input=[{"role": "user", "content": input_prompt}],
            context={'state': state}
        )

        print("Agent Result:", result)
        print("Current State:", state)

        # Update current_agent
        current_agent = result.last_agent

        loop += 1

asyncio.run(main())

save_state_to_json(state, 'testing_session.json')