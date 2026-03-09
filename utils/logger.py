import datetime
import os

LOG_FILE = "agent.log"


def log(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"[{timestamp}] {message}\n"

    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry)
    except Exception:
        pass