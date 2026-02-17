# Twitter/X Post Generator

CLI agent that generates tweet variations for designers, devs, and design engineers. Powered by the Claude Agent SDK.

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

## Custom Tools

| Tool | Description |
|------|-------------|
| `save_drafts` | Saves generated tweets to `drafts.json` |
| `load_past_posts` | Reads `past_posts.txt` for style matching |

Built-in tools: `WebSearch` (trending topics), `WebFetch` (reference content).
