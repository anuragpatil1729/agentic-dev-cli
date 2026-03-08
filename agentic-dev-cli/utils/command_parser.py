def parse_commands(text):

    commands = []

    for line in text.split("\n"):

        line = line.strip()

        if line == "":
            continue

        # remove markdown
        if line.startswith("```"):
            continue

        # remove explanations
        if line.lower().startswith("here"):
            continue

        if line.lower().startswith("sure"):
            continue

        commands.append(line)

    return commands