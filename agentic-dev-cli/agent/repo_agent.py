import os
import re


def handle_repo(prompt, os_type):

    match = re.search(r"https://github.com/\S+", prompt)

    if not match:
        return "echo 'No GitHub repo found'"

    url = match.group()

    repo_name = url.split("/")[-1].replace(".git", "")

    repo_path = os.path.join(os.getcwd(), repo_name)

    commands = []

    # Clone if repo does not exist
    if not os.path.exists(repo_path):

        commands.append(f"git clone {url}")
        commands.append(f"cd {repo_name}")

        return "\n".join(commands)

    # Detect stack
    files = os.listdir(repo_path)

    commands.append(f"cd {repo_name}")

    # Node.js
    if "package.json" in files:

        commands.append("npm install")

        package_path = os.path.join(repo_path, "package.json")

        with open(package_path) as f:
            content = f.read()

        if '"dev"' in content:
            commands.append("npm run dev")

        elif '"start"' in content:
            commands.append("npm start")

        else:
            commands.append("node index.js")

    # Python
    elif "requirements.txt" in files:

        commands.append("pip install -r requirements.txt")

        if "app.py" in files:
            commands.append("python app.py")

        elif "main.py" in files:
            commands.append("python main.py")

    # Streamlit
    elif "streamlit" in str(files).lower():

        commands.append("pip install -r requirements.txt")
        commands.append("streamlit run app.py")

    else:

        commands.append("echo 'Project type not detected'")

    return "\n".join(commands)