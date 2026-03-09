from llm.llama_client import ask_llm
from llm.prompt_templates import planner_prompt


def plan_tasks(user_prompt):

    prompt = user_prompt.strip()

    # ---------------------------------
    # Handle simple commands locally
    # ---------------------------------

    if prompt.startswith("run "):
        return prompt

    if prompt.startswith("setup "):
        return prompt

    if prompt.startswith("install "):
        return prompt

    # ---------------------------------
    # LLM planner for complex prompts
    # ---------------------------------

    system_prompt = planner_prompt(user_prompt)

    response = ask_llm(system_prompt, user_prompt)

    tasks = []

    for line in response.split("\n"):

        line = line.strip()

        if not line:
            continue

        # remove numbering
        if line[0].isdigit():
            line = line.split(".", 1)[1].strip()

        tasks.append(line)

    return " ".join(tasks)