import subprocess


def run_command(command, cwd):

    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # stream stdout
    for line in process.stdout:
        print(line, end="")

    # stream stderr
    for line in process.stderr:
        print(line, end="")

    process.wait()

    return "", "", process.returncode