# Twitter/X Post Generator

CLI agent that generates tweet variations for designers, devs, and design engineers. Powered by the Claude Agent SDK.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- `ANTHROPIC_API_KEY` environment variable

## Setup

```bash
# install dependencies
uv sync

# set your API key
export ANTHROPIC_API_KEY=your-api-key
```

## Usage

```bash
uv run main.py
```

Enter a topic, project description, or design concept. The agent generates 3-4 tweet variations:

- **Punchy/opinionated** — a strong take
- **Educational/tip-style** — a useful insight
- **Conversational/relatable** — community resonance
- **Engagement-optimized** — question or hot take

Drafts are automatically saved to `drafts.json`.

## Style Matching

Edit `past_posts.txt` with your own tweets to have the agent match your voice and writing style.

## Lint and Format

```bash
# format
uv run ruff format .

# lint
uv run ruff check .

# lint and auto-fix
uv run ruff check . --fix
```

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Agent entry point, tools, system prompt, and REPL loop |
| `past_posts.txt` | Example tweets for style matching (edit to match your voice) |
| `drafts.json` | Generated tweet output (created at runtime, gitignored) |

## Tools

| Tool | Description |
|------|-------------|
| `save_drafts` | Saves generated tweets to `drafts.json` |
| `load_past_posts` | Reads `past_posts.txt` for style matching |
| `WebSearch` | Search for trending topics and current data |
| `WebFetch` | Fetch reference content from the web |
