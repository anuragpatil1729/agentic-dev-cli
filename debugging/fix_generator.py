from debugging.error_parser import parse_error


def generate_fix(command, error):

    error_type = parse_error(error)

    if error_type == "permission_error":
        return f"sudo {command}"

    if error_type == "missing_module":

        module = error.split("named")[-1].replace("'", "").strip()

        return f"pip install {module}"

    if error_type == "missing_command":
        return "echo 'Command not found on system'"

    if error_type == "npm_error":
        return "npm install"

    return "echo 'No automatic fix found'"