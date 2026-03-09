import os
import re

VALID_PREFIXES = (
    "pip ",
    "pip3 ",
    "python ",
    "python3 ",
    "npm ",
    "yarn ",
    "node ",
    "git ",
    "docker ",
    "docker-compose ",
    "brew ",
    "curl ",
    "ollama "
)


def extract_setup_commands(repo_path):

    readme_file = None

    for file in os.listdir(repo_path):

        if file.lower().startswith("readme"):
            readme_file = os.path.join(repo_path, file)
            break

    if not readme_file:
        return []

    try:
        with open(readme_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    commands = []

    # find code blocks
    blocks = re.findall(r"```(.*?)```", content, re.DOTALL)

    for block in blocks:

        for line in block.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith(VALID_PREFIXES):
                commands.append(line)

    return commands