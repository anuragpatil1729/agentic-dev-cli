blocked_commands = [
    "rm -rf",
    "shutdown",
    "reboot",
    "mkfs",
    ":(){:|:&};:",  # fork bomb
]


def is_safe(command):

    command = command.lower()

    for bad in blocked_commands:
        if bad in command:
            return False

    return True