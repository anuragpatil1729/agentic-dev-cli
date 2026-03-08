import os

from agent.planner import create_plan
from agent.command_generator import generate_commands
from agent.error_agent import fix_error
from agent.repo_agent import handle_repo

from terminal.executor import run_command
from safety.command_filter import is_safe


print("\n🚀 Agentic Dev CLI\n")

print("Select OS:")
print("1 macOS")
print("2 Ubuntu/Linux")
print("3 Windows")

choice = input("Choice: ")

if choice == "1":
    os_type = "macOS"
elif choice == "2":
    os_type = "Ubuntu"
else:
    os_type = "Windows"

current_dir = os.getcwd()

while True:

    prompt = input("\nAgent > ")

    if prompt.lower() == "exit":
        print("\n👋 Exiting Agent")
        break

    # GitHub repo setup
    if "github.com" in prompt:
        commands = handle_repo(prompt, os_type)

    else:
        plan = create_plan(prompt)
        commands = generate_commands(plan, os_type)

    print("\n📋 Proposed Commands:\n")
    print(commands)

    confirm = input("\nRun these commands? (yes/no): ")

    if confirm.lower() != "yes":
        continue

    for cmd in commands.split("\n"):

        cmd = cmd.strip()

        if cmd == "":
            continue

        # Handle directory change
        if cmd.startswith("cd "):

            new_dir = cmd.replace("cd ", "").strip()

            if os.path.isabs(new_dir):
                current_dir = new_dir
            else:
                current_dir = os.path.join(current_dir, new_dir)

            print("📂 Changed directory to:", current_dir)
            continue

        # Safety check
        if not is_safe(cmd):
            print("❌ Blocked unsafe command:", cmd)
            continue

        print("\n▶ Running:", cmd)

        stdout, stderr, code = run_command(cmd, current_dir)

        if stdout:
            print(stdout)

        if code != 0:

            print("⚠ Error detected:")
            print(stderr)

            fix = fix_error(cmd, stderr)

            print("\n🛠 Suggested fix:")
            print(fix)

            confirm = input("\nRun fix? (yes/no): ")

            if confirm.lower() == "yes":

                print("\n▶ Running fix:", fix)

                run_command(fix, current_dir)