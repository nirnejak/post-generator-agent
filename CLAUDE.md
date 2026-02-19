# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI agent that generates Twitter/X post variations for designers, developers, and design engineers. Built with the Claude Agent SDK. Takes a topic as input via an interactive REPL, generates 3-4 tweet variations in different styles, and streams the output token-by-token to the terminal.

## Commands

```bash
# Install dependencies
uv sync

# Run the agent
uv run main.py

# Lint
uv run ruff check .

# Lint with auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .
```

Requires `ANTHROPIC_API_KEY` environment variable (loaded from `.env` via python-dotenv).

## Architecture

Single-file agent (`main.py`) using the Claude Agent SDK with token-level streaming:

- **MCP Server**: A local SDK MCP server ("posts") exposes one custom tool — `load_past_posts` (reads `past_posts.txt` for voice/style matching).
- **Built-in tools**: The agent also has access to `WebSearch` and `WebFetch` for trending topics and reference content.
- **Streaming**: Uses `include_partial_messages=True` and `StreamEvent` (imported from `claude_agent_sdk.types`, not re-exported from the package root) to stream text deltas in real-time. `AssistantMessage` handling is a no-op since text is already printed via stream events.
- **Interactive REPL**: User enters a topic, agent streams generated tweets, then prompts for the next topic. Exit with `quit`/`exit`/`q` or Ctrl+C.
- **System prompt**: Defines tweet types, rules (280 char limit, no cliché phrases, no gratuitous emojis), and the workflow (load past posts → optionally search web → generate and output directly).

## Key Files

- `main.py` — Agent entry point, tools, system prompt, and REPL loop
- `past_posts.txt` — Example tweets used for style matching (edit to match your voice)

## Tech Stack

- Python 3.12, managed with `uv`
- `claude-agent-sdk` + `python-dotenv`
- `ruff` for linting/formatting (dev dependency)
