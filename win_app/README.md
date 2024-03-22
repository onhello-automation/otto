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

## Create a configuration file
See the sample configuration file [here](./sample_config.yaml).

Make a copy of the sample configuration file and update it with the settings that you would like to use.

## Running the Main Script
Git Bash Example:
```bash
OTTO_LOG_LEVEL=INFO PYTHONPATH="${PWD};${PYTHONPATH}" python otto/main.py ~/otto/config.yaml
```

PowerShell Example:
```powershell
$env:OTTO_LOG_LEVEL="INFO"
$env:PYTHONPATH="${PWD};${env:PYTHONPATH}"
python otto\main.py ${env:USERPROFILE}\otto\config.yaml
```

# Linting
The rules are configuration in [pyproject.toml](pyproject.toml).

To see the changes, run:
```shell
autopep8 --jobs 0 --exit-code .
```

To make the changes automatically, run:
```shell
autopep8 --jobs 0 --in-place .
```
