import os


def detect_stack(repo_path):

    files = os.listdir(repo_path)

    if "package.json" in files:
        return "node"

    if "requirements.txt" in files:
        return "python"

    if "pyproject.toml" in files:
        return "python"

    if "Cargo.toml" in files:
        return "rust"

    if "go.mod" in files:
        return "go"

    if "pom.xml" in files:
        return "java"

    if "Dockerfile" in files:
        return "docker"

    return "unknown"