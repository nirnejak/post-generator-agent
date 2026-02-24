# Twitter/X Post Generator

CLI agent that generates tweet variations for designers, devs, and design engineers. Powered by the Claude Agent SDK with real-time token streaming.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- `ANTHROPIC_API_KEY` environment variable

## Setup

```bash
uv sync
export ANTHROPIC_API_KEY=your-api-key
```

## Usage

```bash
uv run main.py
```

Enter a topic and the agent streams 3-4 tweet variations in real-time:

- **Punchy/opinionated** — a strong take
- **Educational/tip-style** — a useful insight
- **Conversational/relatable** — community resonance
- **Engagement-optimized** — question or hot take

Runs as an interactive REPL — keep entering topics, type `quit` to exit.

## Style Matching

Edit `past_posts.txt` with your own tweets to have the agent match your voice and writing style.

## Development

```bash
uv run ruff format .        # format
uv run ruff check .         # lint
uv run ruff check . --fix   # lint with auto-fix
```
