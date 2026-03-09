import os
import re

from repo.stack_detector import detect_stack
from repo.readme_parser import extract_setup_commands
from docker.docker_detector import detect_docker


def handle_repository(prompt):

    match = re.search(r"https://github.com/\S+", prompt)

    if not match:
        return "echo 'No repository detected'"

    url = match.group()
    repo_name = url.split("/")[-1].replace(".git", "")

    current_dir = os.getcwd()

    commands = []

    # detect if already inside repo
    if os.path.basename(current_dir) == repo_name:
        repo_exists = True
    else:
        repo_exists = os.path.exists(repo_name)

    # ---------------------------------------------------
    # STEP 1: clone repo if it doesn't exist
    # ---------------------------------------------------

    if not repo_exists:

        return "\n".join([
            f"git clone {url}",
            f"cd {repo_name}",
            "echo 'Repository cloned. Run setup again.'"
        ])

    # ---------------------------------------------------
    # STEP 2: ensure we are inside repo
    # ---------------------------------------------------

    if os.path.basename(current_dir) != repo_name:
        commands.append(f"cd {repo_name}")

    repo_path = repo_name

    # ---------------------------------------------------
    # STEP 3: try README instructions
    # ---------------------------------------------------

    readme_cmds = extract_setup_commands(repo_path)

    if readme_cmds:
        commands.extend(readme_cmds)
        return "\n".join(commands)

    # ---------------------------------------------------
    # STEP 4: docker detection
    # ---------------------------------------------------

    docker_type = detect_docker(repo_path)

    if docker_type == "docker":

        commands.append("docker build -t project .")
        commands.append("docker run -p 3000:3000 project")

        return "\n".join(commands)

    if docker_type == "docker-compose":

        commands.append("docker compose up")

        return "\n".join(commands)

    # ---------------------------------------------------
    # STEP 5: detect stack
    # ---------------------------------------------------

    stack = detect_stack(repo_path)

    # ---------------------
    # Node projects
    # ---------------------

    if stack == "node":

        commands.append("npm install")

        if os.path.exists(os.path.join(repo_path, "next.config.js")):
            commands.append("npm run dev")

        elif os.path.exists(os.path.join(repo_path, "vite.config.js")):
            commands.append("npm run dev")

        else:
            commands.append("npm start")

        return "\n".join(commands)

    # ---------------------
    # Python projects
    # ---------------------

    if stack == "python":

        commands.append("pip install -r requirements.txt")

        if os.path.exists(os.path.join(repo_path, "main.py")):
            commands.append("python main.py")

        elif os.path.exists(os.path.join(repo_path, "app.py")):
            commands.append("python app.py")

        elif os.path.exists(os.path.join(repo_path, "server.py")):
            commands.append("python server.py")

        elif os.path.exists(os.path.join(repo_path, "manage.py")):
            commands.append("python manage.py runserver")

        else:
            commands.append("echo 'Python entry file not detected'")

        return "\n".join(commands)

    # ---------------------
    # Go projects
    # ---------------------

    if stack == "go":

        commands.append("go mod tidy")
        commands.append("go run .")

        return "\n".join(commands)

    # ---------------------
    # Rust projects
    # ---------------------

    if stack == "rust":

        commands.append("cargo build")
        commands.append("cargo run")

        return "\n".join(commands)

    # fallback

    commands.append("echo 'Project type not detected'")

    return "\n".join(commands)