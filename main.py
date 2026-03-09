import os
import sys

from agent_controller import AgentController


def main():

    print("\n🚀 Agentic Dev CLI\n")

    print("Select Operating System:")
    print("1. macOS")
    print("2. Ubuntu/Linux")
    print("3. Windows")

    choice = input("Choice: ")

    if choice == "1":
        os_type = "macOS"
    elif choice == "2":
        os_type = "linux"
    else:
        os_type = "windows"

    controller = AgentController(os_type)

    while True:

        prompt = input("\nAgent > ")

        if prompt.lower() in ["exit", "quit"]:
            print("\n👋 Exiting Agent")
            sys.exit()

        controller.handle_prompt(prompt)


if __name__ == "__main__":
    main()