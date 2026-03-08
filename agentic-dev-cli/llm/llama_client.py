import ollama


def ask_llm(system, prompt):

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]