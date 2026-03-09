import os

from agents.planner_agent import plan_tasks
from agents.command_agent import generate_commands
from agents.repo_agent import handle_repository

from execution.executor import run_command
from execution.command_validator import validate

from debugging.fix_generator import generate_fix
from memory.error_memory import get_fix, store_fix

from browser.google_search import search_google
from utils.logger import log


class AgentPipeline:

    def __init__(self, os_type):
        self.os_type = os_type
        self.current_dir = os.getcwd()

    # -------------------------------------------------
    # MAIN PIPELINE
    # -------------------------------------------------

    def process_prompt(self, prompt):

        # ---------------------------------------------
        # Repo handling
        # ---------------------------------------------

        if "github.com" in prompt:
            commands = handle_repository(prompt)

        else:
            tasks = plan_tasks(prompt)
            commands = generate_commands(tasks, self.os_type)

        print("\n📋 Proposed Commands:\n")
        print(commands)

        confirm = input("\nRun commands? (yes/no): ")

        if confirm != "yes":
            return

        # ---------------------------------------------
        # Deduplicate commands
        # ---------------------------------------------

        command_list = []
        seen = set()

        for line in commands.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line in seen:
                continue

            seen.add(line)
            command_list.append(line)

        # ---------------------------------------------
        # Execute commands
        # ---------------------------------------------

        for cmd in command_list:

            # ignore README menu text
            if cmd.startswith(("1.", "2.", "3.", "4.")):
                continue

            if "├" in cmd or "│" in cmd:
                continue

            if cmd.startswith("```"):
                continue

            # avoid repeated ollama serve
            if "ollama serve" in cmd:
                continue

            # -----------------------------------------
            # handle directory change
            # -----------------------------------------

            if cmd.startswith("cd "):

                folder = cmd.replace("cd ", "").strip()

                new_path = os.path.join(self.current_dir, folder)

                if os.path.exists(new_path):

                    self.current_dir = new_path
                    print("📂 Changed directory:", self.current_dir)

                else:

                    print("⚠ Directory not found:", folder)

                continue

            # -----------------------------------------
            # safety validation
            # -----------------------------------------

            if not validate(cmd):

                print("❌ Blocked command:", cmd)
                continue

            # -----------------------------------------
            # execute
            # -----------------------------------------

            print("\n▶ Running:", cmd)

            stdout, stderr, code = run_command(cmd, self.current_dir)

            log(f"CMD: {cmd}")
            log(stdout)
            log(stderr)

            if stdout:
                print(stdout)

            if code != 0:

                print("⚠ Error detected")

                if stderr:
                    print("\n----- ERROR OUTPUT -----")
                    print(stderr)
                    print("------------------------")

                error = stderr.strip()

                # ---------------------------------
                # Check memory fixes
                # ---------------------------------

                fix = get_fix(error)

                if not fix:
                    fix = generate_fix(cmd, error)

                if not fix:

                    search_google(error)

                    fix = "echo 'No automatic fix found'"

                print("\n🛠 Suggested fix:")
                print(fix)

                confirm = input("Run fix? (yes/no): ")

                if confirm == "yes":

                    print("\n▶ Running:", fix)

                    run_command(fix, self.current_dir)

                    store_fix(error, fix)