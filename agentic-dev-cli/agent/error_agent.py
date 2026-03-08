from llm.llama_client import ask_llm


def fix_error(command, error):

    system_prompt = """
A terminal command failed.

Return ONLY the corrected command.

Rules:
- no explanations
- no markdown
- no text
- only the corrected command
"""

    prompt = f"""
Command:
{command}

Error:
{error}
"""

    response = ask_llm(system_prompt, prompt)

    # clean response
    response = response.replace("```", "")
    response = response.replace("bash", "")

    return response.strip()