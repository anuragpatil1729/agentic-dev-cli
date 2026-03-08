from llm.llama_client import ask_llm


def generate_commands(plan, os_type):

    commands = []

    for step in plan:

        system = f"""
Convert the task into terminal commands.

OS: {os_type}

Rules:
- output only commands
- one command per line
- no explanations
"""

        response = ask_llm(system, step)

        commands.append(response)

    return "\n".join(commands)