import subprocess


def run_command(command, cwd=None):

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        return stdout, stderr, process.returncode

    except Exception as e:

        return "", str(e), 1