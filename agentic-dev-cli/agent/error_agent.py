import os

from llm.llama_client import ask_llm
from memory.error_memory import get_fix, store_fix
from browser.search_agent import search_google


def fix_error(command, error):

    error_text = error.lower()

    # -------------------------
    # 1 memory fixes
    # -------------------------

    saved_fix = get_fix(error_text)

    if saved_fix:

        print("🧠 Using stored fix")
        return saved_fix

    # -------------------------
    # 2 Next.js fixes
    # -------------------------

    if "turbopack" in error_text or "next.js" in error_text:

        fix = "rm -rf node_modules .next && npm install && npm run dev"

        store_fix("nextjs_cache_error", fix)

        return fix

    # -------------------------
    # 3 npm errors
    # -------------------------

    if "npm err" in error_text:

        fix = "npm install"

        store_fix("npm_install_error", fix)

        return fix

    # -------------------------
    # 4 python errors
    # -------------------------

    if "modulenotfounderror" in error_text:

        parts = error_text.split("named")

        if len(parts) > 1:

            module = parts[1].replace("'", "").strip()

            fix = f"pip install {module}"

            store_fix("python_missing_module", fix)

            return fix

    # -------------------------
    # 5 permission errors
    # -------------------------

    if "permission denied" in error_text:

        fix = f"sudo {command}"

        store_fix("permission_error", fix)

        return fix

    # -------------------------
    # 6 LLM reasoning
    # -------------------------

    system_prompt = """
A terminal command failed.

Return ONLY the corrected bash command.

No explanation.
Only the command.
"""

    prompt = f"""
Command:
{command}

Error:
{error}
"""

    response = ask_llm(system_prompt, prompt)

    response = response.replace("```", "").replace("bash", "")

    fix = response.strip()

    if fix:
        store_fix(error_text[:60], fix)
        return fix

    # -------------------------
    # 7 GOOGLE SEARCH FALLBACK
    # -------------------------

    search_google(error)

    return "echo 'Opened browser to search for fix'"