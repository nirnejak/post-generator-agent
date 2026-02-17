# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI agent that generates Twitter/X post variations for designers, developers, and design engineers. Built with the Claude Agent SDK. Takes a topic as input, generates 3-4 tweet variations in different styles (punchy, educational, conversational, engagement-optimized), and saves drafts to `drafts.json`.

## Commands

```bash
# Install dependencies
uv sync

# Run the agent
uv run main.py
```

Requires `ANTHROPIC_API_KEY` environment variable to be set.

## Architecture

This is a single-file agent (`main.py`) using the Claude Agent SDK:

- **MCP Server**: A local SDK MCP server ("posts") exposes two custom tools — `save_drafts` (appends generated tweets to `drafts.json`) and `load_past_posts` (reads `past_posts.txt` for voice/style matching).
- **Built-in tools**: The agent also has access to `WebSearch` and `WebFetch` for trending topics and reference content.
- **Interactive loop**: The agent runs in a REPL — user enters a topic, agent generates tweets, saves them, and waits for the next input.
- **System prompt**: Defines tweet types, rules (280 char limit, no cliché phrases, no gratuitous emojis), and the workflow (load past posts → optionally search web → generate → save).

## Key Files

- `main.py` — Agent entry point, tools, system prompt, and REPL loop
- `past_posts.txt` — Example tweets used for style matching (edit to match your voice)
- `drafts.json` — Generated tweet output (gitignored, created at runtime)

## Tech Stack

- Python 3.12, managed with `uv`
- `claude-agent-sdk` as the sole dependency
