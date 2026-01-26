"""Interactive OpenAI Agents SDK Socratic agent.

Termination condition:
- Stop immediately if the user types `resolved`.
- Otherwise, stop after 5 user turns.

Important:
- Run with the project virtualenv so you import OpenAI's Agents SDK, not the unrelated
  TensorFlow RL package named `agents`.

Example:
    .venv/bin/python socratic_llm.py
"""

from __future__ import annotations

from agents import Agent, Runner


MAX_USER_TURNS = 10
RESOLVED_TOKEN = "resolved"


def main() -> None:
    socratic_agent = Agent(
        name="Socratic Agent",
        handoff_description=(
            "An agent that uses Socratic questioning to guide users to solving problems on their own."
        ),
        model="gpt-4o-mini",
        instructions=(
            """
You are a Socratic Agent. Your goal is to help users arrive at their
own conclusions through a series of thoughtful questions. Avoid giving direct
answers; instead, ask questions that encourage critical thinking and 
self-reflection.

When responding, consider the following guidelines:
1. Start by understanding the user's problem or question.
2. Ask open-ended questions that prompt the user to think deeply about the issue.
3. Avoid leading questions that suggest a specific answer.
4. Encourage the user to explore different perspectives and possibilities.
5. Summarize the user's thoughts periodically to ensure understanding and to help them see their own reasoning process.
You may provide theoretical explanation if it is directly related to the student’s request.
"""
        ),
    )

    print(
        "Socratic Agent (type 'resolved' when you're done).\n"
        f"I will stop after {MAX_USER_TURNS} turns if you don't mark it resolved.\n"
    )
    previous_response_id: str | None = None

    user_turns = 0
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if not user_input:
            continue

        if user_input.lower() == RESOLVED_TOKEN:
            print("Marked as resolved. Bye!")
            return

        user_turns += 1

        result = Runner.run_sync(
            socratic_agent,
            user_input,
            previous_response_id=previous_response_id,        )

        print(f"Agent: {result.final_output}\n")
        previous_response_id = result.last_response_id

        if user_turns >= MAX_USER_TURNS:
            print(
                "Stopping: you have taken 5 turns with the user, and the user has not marked the problem as resolved."
            )
            return


if __name__ == "__main__":
    main()
