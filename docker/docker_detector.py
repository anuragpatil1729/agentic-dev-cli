import os


def detect_docker(repo_path):

    try:
        files = os.listdir(repo_path)
    except Exception:
        return None

    if "Dockerfile" in files:
        return "docker"

    if "docker-compose.yml" in files or "compose.yml" in files:
        return "docker-compose"

    return None