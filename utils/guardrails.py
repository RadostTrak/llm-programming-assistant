import re
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    output_guardrail
)

@output_guardrail
async def code_detection_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str
) -> GuardrailFunctionOutput:
    """
    Detect if agent response contains code.
    If code is detected, tripwire is triggered and agent must retry.
    """
    response = output
    violations = []
    
    # Check for code blocks
    if '```' in response:
        violations.append("code block markers (```)")
    
    # Check for common code patterns
    code_patterns = [
        (r'\bdef\s+\w+\s*\(', 'function definition'),
        (r'\bfor\s+\w+\s+in\s+range\(', 'for loop'),
        (r'\bif\s+.+:\s*\n', 'if statement'),
        (r'\bwhile\s+.+:\s*\n', 'while loop'),
        (r'\w+\s*=\s*\[.*\]', 'list assignment'),
        (r'\bvar\s+\w+\s*=', 'var declaration'),
        (r'\blet\s+\w+\s*=', 'let declaration'),
        (r'\bconst\s+\w+\s*=', 'const declaration'),
        (r'\bfunction\s+\w+\s*\(', 'function keyword'),
        (r'=>\s*{', 'arrow function'),
    ]
    
    for pattern, description in code_patterns:
        if re.search(pattern, response, re.MULTILINE | re.IGNORECASE):
            violations.append(description)
    
    # Check for suspicious inline code
    inline_code_matches = re.findall(r'`([^`]+)`', response)
    for match in inline_code_matches:
        if len(match) > 15 or any(char in match for char in ['=', '(', ')', '[', ']', '{', '}']):
            violations.append("code snippet in backticks")
            break
    
    # Determine if code was detected
    code_detected = len(violations) > 0
    
    # Create output info message
    if code_detected:
        output_info = (
            f"CODE VIOLATION DETECTED: {', '.join(set(violations))}. "
            "You MUST NOT provide any code snippets, code blocks, or programming syntax. "
            "Revise your response to guide with questions and conceptual explanations only."
        )
    else:
        output_info = "Response is safe - no code detected."
    
    return GuardrailFunctionOutput(
        output_info=output_info,
        tripwire_triggered=code_detected  # True = reject response, agent retries
    )