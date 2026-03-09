import os
import shutil


def generate_commands(tasks, os_type):

    if isinstance(tasks, list):
        tasks = " ".join(tasks)

    tasks = tasks.strip()

    cwd = os.getcwd()

    # -----------------------------
    # RUN COMMAND
    # -----------------------------

    if tasks.startswith("run "):

        target = tasks.replace("run ", "").strip()

        # handle ./ executables
        if target.startswith("./"):

            full_path = os.path.join(cwd, target[2:])

            if os.path.exists(full_path):
                return target

        # local file
        full_path = os.path.join(cwd, target)

        if os.path.exists(full_path):
            return f"./{target}"

        # bin executable
        bin_path = os.path.join(cwd, "bin", target)

        if os.path.exists(bin_path):
            return f"./bin/{target}"

        # system command
        if shutil.which(target.split()[0]):
            return target

        return f"echo 'Command not found: {target}'"

    # -----------------------------
    # SETUP REPOSITORY
    # -----------------------------

    if tasks.startswith("setup "):

        repo = tasks.replace("setup ", "").strip()

        if repo.startswith("http"):
            return f"git clone {repo}"

        return "echo 'Invalid repository URL'"

    # -----------------------------
    # INSTALL COMMAND
    # -----------------------------

    if tasks.startswith("install "):

        pkg = tasks.replace("install ", "").strip()

        return f"pip install {pkg}"

    # -----------------------------
    # FALLBACK
    # -----------------------------

    return f"echo 'Task not recognized: {tasks}'"