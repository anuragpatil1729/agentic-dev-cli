import os
import re


def handle_repo(prompt, os_type):

    # extract github url
    match = re.search(r"https://github.com/\S+", prompt)

    if not match:
        return "echo 'No GitHub repo found in prompt'"

    url = match.group()

    repo_name = url.split("/")[-1].replace(".git", "")

    repo_path = os.path.join(os.getcwd(), repo_name)

    commands = []

    # clone if not exists
    if not os.path.exists(repo_path):

        commands.append(f"git clone {url}")
        commands.append(f"cd {repo_name}")

        # stack detection will happen after clone
        commands.append("echo 'Repo cloned. Run setup again to detect stack.'")

        return "\n".join(commands)

    # repo already exists → detect stack
    files = os.listdir(repo_path)

    commands.append(f"cd {repo_name}")

    if "package.json" in files:

        commands.append("npm install")

        package_file = os.path.join(repo_path, "package.json")

        with open(package_file) as f:
            content = f.read()

            if '"dev"' in content:
                commands.append("npm run dev")

            elif '"start"' in content:
                commands.append("npm start")

            else:
                commands.append("node server.js")

    elif "requirements.txt" in files:

        commands.append("pip install -r requirements.txt")
        commands.append("python main.py")

    else:

        commands.append("echo 'Project type not detected'")

    return "\n".join(commands)