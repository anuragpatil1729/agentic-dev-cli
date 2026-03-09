BLOCKED_COMMANDS = [
    "rm -rf /",
    "shutdown",
    "reboot",
    "mkfs",
    ":(){:|:&};:",  # fork bomb
    "dd if="
]


def validate(command):

    cmd = command.lower()

    for bad in BLOCKED_COMMANDS:

        if bad in cmd:
            return False

    return True