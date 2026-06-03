# CLI-Task-Tracker
A command-line task manager built in Python as a learning project. The focus is on clean, typed, production-oriented code using dataclasses, JSON-based persistence, and a modular project structure with a properly packaged CLI entry point.

## Stack

| Component | Details |
|---|---|
| Language | Python 3.13.3 |
| Persistence | JSON file-based storage (`tasks.json`) |
| Core libraries | `dataclasses`, `pathlib`, `typing`, `datetime`, `argparse` |
| Testing | `pytest` |
| Packaging | `setuptools`, `pyproject.toml` |

## Installation

```bash
# 1. Clone the repository and navigate into it
git clone https://github.com/fhitzke/CLI-Task-Tracker.git
cd CLI-Task-Tracker

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install setuptools and the package
pip install setuptools
pip install -e .
```

After installation, the `task-tracker` command is available globally within the virtual environment.

## Usage

```bash
task-tracker add "Walk the dog"
task-tracker update 0 "Walk the dog and cook dinner"
task-tracker delete 0
task-tracker status 0 "done"
task-tracker list
task-tracker list "in-progress"
task-tracker list "done"
```

## Commands

| Command | Arguments | Description |
|---|---|---|
| `add` | `<description>` | Add a new task |
| `update` | `<id> <description>` | Update the description of an existing task |
| `delete` | `<id>` | Delete a task by ID |
| `change-status` | `<id> <status>` | Set task status (`in-progress`, `done`) |
| `list` | `[status]` | List all tasks, optionally filtered by status |

## Project Structure

```
CLI-Task-Tracker/
├── src/
│   ├── __init__.py
│   ├── core.py           # CLI entry point and argument parsing
│   ├── cli_task_tracker.py  # TaskTracker dataclass and business logic
│   └── task.py           # Task dataclass definition
├── tests/
│   ├── __init__.py
│   ├── test_task_tracker.py # TaskTracker testing
│   └── test_task.py # Task testing
├── main.py
├── pyproject.toml
└── tasks.json
```

## Testing

```bash
pytest
```

Tests cover task creation, updating, deletion, status changes, persistence, and error handling. The test suite uses `pytest.raises` for exception assertions and `unittest.mock.patch` for time-dependent behavior.

Note: tests require an empty or non-existent `tasks.json` file to run correctly. Each test cleans up after itself via `purge_task_registry()`.

## Design Principles

- **Typing**: Every function and method is fully annotated using `typing` and `dataclasses`
- **Persistence**: Tasks are stored in a JSON file and fully restored on initialization, including datetime deserialisation
- **Separation of concerns**: CLI parsing, business logic, and data modelling are split across distinct modules
- **Testability**: The classes `TaskTracker` and `Task` are independently instantiable and testable without invoking the CLI