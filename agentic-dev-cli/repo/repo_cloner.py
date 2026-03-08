from terminal.executor import run_command


def clone_repo(url, cwd):

    command = f"git clone {url}"

    print("\n📦 Cloning repository...\n")

    run_command(command, cwd)