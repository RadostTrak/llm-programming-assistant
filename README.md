# LLM Programming Assistant Prototype
A multi-agent programming assistant that helps students debug their Python code through guided questioning rather than providing answers directly. Built using [OpenAI's Agents SDK](https://github.com/openai/openai-agents-python) for an academic internship on integrating LLM assistants into introductory programming education.

This repository is the architecture prototype used to validate the multi-agent system before integrating it into a larger web application. 

## Architecture
The system uses three agents -- Triage, Diagnostic, and Socratic -- that collaborate through a shared `DebuggingState` object.
- Triage Agent - Collects info about the student's issue and transfers to Diagnostic once it has enough information.
- Diagnostic Agent - Identifies the root cause of the student's error and produces a learning plan for Socratic to follow. Can request more information from Triage or revise its plan based on feedback from Socratic.
- Socratic Agent - Executes the diagnostic plan by asking the student guiding questions that do not reveal the solution.
The agents read from and write to a single `DebuggingState` dataclass, which tracks exercise context, each agent's findings, the current diagnostic plan, and handoff history. Agent transfers are generated through a factory function that creates named handoff tools and records each transfer with its reason and timestamp in the shared state.

The production version includes further refinements to prompts and UI integration.