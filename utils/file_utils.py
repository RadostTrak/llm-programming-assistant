import json
import yaml
from state import DebuggingState


def save_all_exercises_to_json(yaml_filepath: str, json_filepath: str = 'starting_state.json'):
    """
    Convert all exercises from YAML to JSON format.
    Creates an array of initial states, one per exercise.
    
    Args:
        yaml_filepath: Path to YAML file (e.g., 'problemset.yaml')
        json_filepath: Path for output JSON (default: 'starting_state.json')
    """
    # Read YAML file
    with open(yaml_filepath, 'r') as file:
        exercise_data = yaml.safe_load(file)
    
    # Create initial state for each exercise
    exercises = []
    for exercise in exercise_data["exercises"]:
        state = DebuggingState()
        state.broad_context = exercise_data["context"].strip()
        state.exercise_id = exercise['id']
        state.exercise_title = exercise['title']
        state.exercise_prompt = exercise['prompt'].strip().replace('\n', " ")
        state.exercise_context = exercise['context'].strip()
        exercises.append(state.to_dict())
    
    # Save to JSON
    with open(json_filepath, 'w') as file:
        json.dump(exercises, file, indent=2)


def save_state_to_json(state: DebuggingState, filepath: str):
    """Save debugging state to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(state.to_dict(), f, indent=2)


def load_state_from_json(filepath: str) -> DebuggingState:
    """Load debugging state from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return DebuggingState.from_dict(data)


def load_exercise_from_yaml(yaml_filepath: str, exercise_id: str) -> DebuggingState:
    """
    Load a specific exercise from YAML into a new DebuggingState.

    Args:
        yaml_filepath: Path to exercises YAML file (e.g., 'problemset.yaml')
        exercise_id: ID of the exercise to load (e.g., "1.1")

    Returns:
        DebuggingState with exercise loaded
    """
    # Read YAML file
    with open(yaml_filepath, 'r') as file:
        exercise_data = yaml.safe_load(file)

    # Find the specific exercise
    exercise = None
    for ex in exercise_data["exercises"]:
        if str(ex['id']) == str(exercise_id):
            exercise = ex
            break

    if not exercise:
        raise ValueError(f"Exercise {exercise_id} not found in {yaml_filepath}")

    # Create state with exercise loaded
    state = DebuggingState()
    state.broad_context = exercise_data["context"].strip()
    state.exercise_id = exercise['id']
    state.exercise_title = exercise['title']
    state.exercise_prompt = exercise['prompt'].strip().replace('\n', " ")
    state.exercise_context = exercise['context'].strip()

    return state


def load_all_exercises_from_yaml(yaml_filepath: str) -> list[DebuggingState]:
    """
    Load all exercises from YAML as separate DebuggingState objects.

    Returns:
        List of DebuggingState objects, one per exercise
    """
    with open(yaml_filepath, 'r') as f:
        data = yaml.safe_load(f)

    states = []
    for exercise in data.get('exercises', []):
        state = DebuggingState()
        state.broad_context = data.get('context', '')
        state.exercise_id = str(exercise['id'])
        state.exercise_title = exercise['title']
        state.exercise_prompt = exercise['prompt']
        state.exercise_context = exercise['context']
        states.append(state)

    return states

