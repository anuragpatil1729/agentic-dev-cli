import subprocess


def ask_llm(system_prompt, user_prompt):

    prompt = system_prompt + "\n\n" + user_prompt

    try:

        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as e:

        print("LLM error:", e)

        return ""