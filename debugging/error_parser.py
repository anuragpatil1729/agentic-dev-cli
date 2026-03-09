def parse_error(stderr):

    if not stderr:
        return "unknown"

    error = stderr.lower()

    if "permission denied" in error:
        return "permission_error"

    if "module not found" in error:
        return "missing_module"

    if "command not found" in error:
        return "missing_command"

    if "npm err" in error:
        return "npm_error"

    return "unknown"