# AI Pipelines for Direct Democracy Forum
This repo is essentially my test-bed for the AI pipelines used on https://directdemocracyforum.com. Right now there is only one such pipeline, the bill "enrichment" workflow, that uses an API call to pre-fill various fields on the forum linked to a newly published bill. In my production application, this is bundled into a Celery-orchestrated pipeline. In this repo, you can see the prompt and API call that I make, and some of the experiments I have done.

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

3. Get a Google Gemini API key, then add it to a `.env` file.

## Usage

The following command currently runs the bill-enrichment pipeline on a large dataset of bills:

```
python run.py
```