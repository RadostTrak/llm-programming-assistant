from agents import Agent, Runner
from pydantic import BaseModel

# Greeter Agent Example (Synchronous)
agent = Agent(
    name = 'Basic Agent',
    instructions = 'You are a greeter bot. Greet the user warmly with their name.',
    model = 'gpt-5-nano'
)

result = Runner.run_sync(agent, 'Hello, my name is Radost. How are you?')
print(result.final_output)

## Recipe Agent Example
class Recipe(BaseModel):
    title: str
    ingredients: list[str]
    cooking_time: int
    servings: int

recipe_agent = Agent(
    name = 'Recipe Agent',
    instructions = ('You are a helpful assistant that provides recipes based on user requests.'
                    'The cooking time should be in minutes'),
    output_type = Recipe,
    model = 'gpt-5-nano'
)

response = Runner.run_sync(recipe_agent, 'Dish that uses spinach, thai red curry paste, and has yellow split peas as the base ingredient.')
recipe = response.final_output
print(recipe)