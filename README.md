# 🚀 Agentic Dev CLI

An intelligent command-line agent that automates software development workflows using LLMs. It can clone repositories, detect project stacks, execute commands, handle errors, and learn from past fixes.

## Features

✨ **Core Capabilities**
- 🤖 **AI-Powered Task Planning** - Converts natural language requests into executable commands
- 📦 **Repository Automation** - Automatically clones, sets up, and runs GitHub repositories
- 🔍 **Stack Detection** - Identifies project type (Node, Python, Go, Rust, Java, Docker)
- 💾 **Error Learning** - Remembers and reuses fixes for recurring errors
- 🛡️ **Safety Validation** - Prevents execution of dangerous commands
- 🔧 **Smart Error Recovery** - Automatically generates and suggests fixes

## Supported Technologies

**Languages & Runtimes:**
- Python (pip, requirements.txt)
- Node.js (npm, package.json)
- Go (go.mod)
- Rust (Cargo.toml)
- Java (Maven)

**DevOps:**
- Docker & Docker Compose
- Git

**Package Managers:**
- pip / pip3
- npm / yarn
- brew (macOS)

**Operating Systems:**
- macOS
- Ubuntu/Linux
- Windows

## Installation

### Prerequisites
- Python 3.8+
- Ollama (for local LLM support)
- Git

### Setup

```bash
# Clone this repository
git clone https://github.com/yourusername/agentic-dev-cli.git
cd agentic-dev-cli

# Install dependencies
pip install -r requirements.txt

# Start Ollama service
ollama pull llama3
ollama serve
```

### Install Ollama

**macOS:**
```bash
brew install ollama
brew services start ollama
ollama pull llama3
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

## Usage

### Starting the Agent

```bash
python main.py
```

You'll be prompted to select your OS:
```
🚀 Agentic Dev CLI

Select Operating System:
1. macOS
2. Ubuntu/Linux
3. Windows

Choice: 1
```

### Command Examples

#### Clone & Setup a Repository
```
Agent > setup https://github.com/Vishwesh-Bhilare/ReachlyEngine.git
```
The agent will:
1. Clone the repository
2. Detect the project type
3. Extract setup commands from README
4. Execute the setup pipeline

#### Run an Executable
```
Agent > run ./bin/reachly
```

#### Install a Package
```
Agent > install requests
```

#### Execute Custom Commands
```
Agent > create a Python script that prints "Hello World"
Agent > start the development server
```

## Architecture

### Agent Pipeline

```
User Input
    ↓
[Planner Agent] - Breaks down complex tasks
    ↓
[Command Agent] - Generates terminal commands
    ↓
[Repo Agent] - Handles repository setup
    ↓
[Executor] - Runs commands safely
    ↓
[Error Handler] - Detects & fixes failures
    ↓
[Memory] - Learns from past fixes
```

### Key Modules

#### `agents/`
- **planner_agent.py** - AI-powered task planning using Llama3
- **command_agent.py** - Converts tasks to shell commands
- **repo_agent.py** - Repository detection and setup orchestration

#### `execution/`
- **executor.py** - Subprocess management
- **command_validator.py** - Safety checks before execution

#### `debugging/`
- **error_parser.py** - Categorizes errors
- **fix_generator.py** - Creates fixes based on error type

#### `memory/`
- **error_memory.py** - Persistent error-fix mapping in JSON

#### `repo/`
- **stack_detector.py** - Identifies project type from files
- **readme_parser.py** - Extracts setup commands from READMEs

## Configuration

### Settings

Edit `config/settings.py` to customize:

```python
MODEL = "llama3"  # LLM model to use

SUPPORTED_OS = [
    "macOS",
    "Ubuntu",
    "Windows"
]

SAFE_COMMANDS = [
    "git", "npm", "pip", "brew", "apt", "docker"
]
```

### Blocked Commands

Safety rules are enforced in `execution/command_validator.py`:

```python
BLOCKED_COMMANDS = [
    "rm -rf /",      # Prevent system deletion
    "shutdown",      # Prevent system shutdown
    "reboot",        # Prevent reboots
    "mkfs",          # Prevent filesystem formatting
    ":(){:|:&};:",   # Fork bomb
    "dd if="         # Prevent disk writes
]
```

## Error Handling

The agent automatically handles common errors:

| Error Type | Auto-Fix |
|-----------|----------|
| `permission_error` | Prepends `sudo` |
| `missing_module` | Runs `pip install <module>` |
| `missing_command` | Suggests installation |
| `npm_error` | Runs `npm install` |

### Error Memory

The agent stores fixes in `memory/fix_database.json`:

```json
{
  "python: can't open file": "echo 'No automatic fix found'",
  "fatal: destination path exists": "rm -rf <dir> && git clone <url>"
}
```

When an error occurs again, the agent retrieves and applies the stored fix.

## Development

### Project Structure

```
agentic-dev-cli/
├── agents/              # AI agents for planning & commands
├── execution/           # Command execution & validation
├── debugging/           # Error parsing & fixing
├── memory/              # Error-fix database
├── repo/                # Repository analysis
├── docker/              # Docker detection
├── environment/         # Runtime detection
├── llm/                 # Ollama integration
├── utils/               # Helpers & logging
├── config/              # Settings & configuration
├── tests/               # Test suite
├── ui/                  # Web dashboard (future)
├── main.py              # Entry point
├── agent_controller.py  # Main orchestrator
└── agent_pipeline.py    # Execution pipeline
```

### Testing

```bash
# Run tests
python -m pytest tests/

# Test a specific module
python -m pytest tests/test_repo_agent.py
```

### Adding a New Agent

1. Create `agents/new_agent.py`:
```python
def handle_something(prompt):
    # Implementation
    return result
```

2. Integrate in `agent_pipeline.py`:
```python
from agents.new_agent import handle_something

if "keyword" in prompt:
    commands = handle_something(prompt)
```

## Logging

All operations are logged to `agent.log`:

```
[2026-03-09 18:39:04] CMD: ./ReachlyEngine/bin/reachly
[2026-03-09 18:39:04] [INFO] main: LinkedIn authentication already present
[2026-03-09 18:39:04] RuntimeError: Ollama not running or model missing
```

View logs:
```bash
tail -f agent.log
```

## API Reference

### AgentController

```python
from agent_controller import AgentController

controller = AgentController("macOS")
response = controller.handle_prompt("setup https://github.com/user/repo.git")
```

### AgentPipeline

```python
from agent_pipeline import AgentPipeline

pipeline = AgentPipeline("linux")
stdout, stderr, code = pipeline.process_prompt("run python main.py")
```

### Executor

```python
from execution.executor import run_command

stdout, stderr, code = run_command("git clone <url>", "/path/to/dir")
```

## Troubleshooting

### Issue: "Ollama not running or model missing"
```bash
# Ensure Ollama is running
ollama serve

# In another terminal, pull the model
ollama pull llama3

# Verify
ollama list
```

### Issue: "Repository already exists"
```bash
# Remove existing directory
rm -rf <repo_name>

# Try again
```

### Issue: Permission denied
The agent will automatically prepend `sudo` for permission errors.

### Issue: Commands not executing
Check `execution/command_validator.py` - the command may be blocked for safety reasons.

## Performance Tips

1. **Use Local LLM** - Ollama runs locally, no API costs
2. **Memory Learning** - Later runs benefit from cached fixes
3. **Validate Early** - Safety checks happen before execution
4. **Stream Output** - Commands stream output in real-time

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Web UI dashboard
- [ ] More error fix patterns
- [ ] Support for more languages (Ruby, PHP, etc.)
- [ ] Parallel command execution
- [ ] Custom plugin system
- [ ] Comprehensive test coverage

## Roadmap

- **v0.2** - Web dashboard
- **v0.3** - Multi-language plugin system
- **v0.4** - Cloud LLM integration (OpenAI, Claude)
- **v0.5** - Team collaboration features
- **v1.0** - Production release

## License

MIT License - see LICENSE file

## Support

- 📖 [Documentation](./docs)
- 🐛 [Report Issues](https://github.com/yourusername/agentic-dev-cli/issues)
- 💬 [Discussions](https://github.com/yourusername/agentic-dev-cli/discussions)

## Acknowledgments

- Built with [Ollama](https://ollama.com/) for local LLM inference
- Inspired by [GitHub Actions](https://github.com/features/actions) and [CodeWhisperer](https://aws.amazon.com/codewhisperer/)

---

**Made with ❤️ for developers who automate their workflows**
