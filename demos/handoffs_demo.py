from agents import Agent, Runner
from pydantic import BaseModel

## First generate an outline, then build a tutorial on markdown

class Tutorial(BaseModel):
    outline: str
    tutorial: str

# Because the outline agent hands off to the tutorial generator agent, define tutorial generator first
# Tutorial generator has access to both outline builder's output and the tutorial it generates
tutorial_generator = Agent(
    name='Tutorial Generator',
    model='gpt-5-nano',
    handoff_description='Used for generating a tutorial based on an outline',
    instructions=(
        'Given a programming topic and an outline, your job is to generate a tutorial to explain the topic.'
        'The topic should be suited to beginners learning programming for the first time, and contain no jargon.'
        'Where it makes sense, include code snippets to illustrate concepts.'
        'Format the outline and tutorial in markdown.'
    ),
    # Return the output in the way specified by the Tutorial pydantic model
    output_type=Tutorial
)

outline_builder = Agent(
    name='Outline Builder',
    model='gpt-5-nano',
    instructions=(
        'You are a helper agent that makes tutorials that assist students learning introductory programming.'
        'Given a particular programming topic, your job is to help come up with an outline for a tutorial on that topic.'
        'After making the outline, hand it to the tutorial generator agent'
        ),
    handoffs=[tutorial_generator] # handoffs does not necessarily hand off
)

tutorial_response = Runner.run_sync(outline_builder, 'Modulo operator in Python')
print(tutorial_response.final_output)