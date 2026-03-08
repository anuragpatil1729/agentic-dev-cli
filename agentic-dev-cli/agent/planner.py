from llm.llama_client import ask_llm


def create_plan(prompt):

    system = """
Break the user request into installation steps.

Rules:
- short steps
- numbered list
- no explanations
"""

    response = ask_llm(system, prompt)

    steps = []

    for line in response.split("\n"):

        line = line.strip()

        if line == "":
            continue

        # remove numbers
        if "." in line:
            line = line.split(".", 1)[1].strip()

        steps.append(line)

    return steps