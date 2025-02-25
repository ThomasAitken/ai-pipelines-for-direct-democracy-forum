# AI Pipelines for Direct Democracy Forum
This repo shows how I generate AI completions for the bill forums on https://directdemocracyforum.com. I have since turned this process into a Celery-orchestrated pipeline that lives inside the main (private) repo. However, I will keep this repo up to date as I change my prompts, or create new AI experiments for the forum.

## Installation

1. Install uv
If uv is not already installed on the new machine:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Set up virtual env and dependencies
```
uv venv
uv sync
source .venv/bin/activate
```

3. Get your own API key for OpenAI or one of the other providers, then add it to a `.env` file. Add credit.

## Usage

The following runs the bill-enrichment pipeline currently:

```
python run.py
```