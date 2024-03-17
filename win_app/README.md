# otto
Help AI control your PC.

This might only work on Windows because we use `pywinauto` to control applications.
It might work on Linux too.

# Plans
## RAG
- Support providing a folder of documents for context.

## Decision Making
- Use LLM to decide what to do. Start with Ollama + SK. Make a generic connector interface so that other options can be used too.

## Actions
### Teams
- ✅ Support writing a message in a Teams chat.
- Get the latest messages in a Teams chat for context to LLM.

### Code
- Support editing code in VS Code.
- Support editing code in ADO.

# Setup
See the steps below to setup this project.

## Setup Python
Use Python 3.11.
Example:
```shell
conda create --yes --name otto python=3.11
conda activate otto
```

## Install Poetry
See [here](https://python-poetry.org/docs/main).

## Install Dependencies
```shell
poetry install
```

# Running
Make sure the environment is activated.
For example, if you are using Conda:
```shell
conda activate otto
```

## Running the Main Script
Git Bash Example:
```bash
OTTO_LOG_LEVEL=INFO PYTHONPATH="${PWD};${PYTHONPATH}" python otto/main.py
```

PowerShell Example:
```powershell
$env:OTTO_LOG_LEVEL="INFO"
$env:PYTHONPATH="${PWD};${env:PYTHONPATH}"
python otto\main.py
```
