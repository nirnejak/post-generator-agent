import asyncio
import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)

DRAFTS_FILE = "drafts.json"
PAST_POSTS_FILE = "past_posts.txt"


@tool(
    "save_drafts",
    "Save generated tweet drafts to a JSON file. Call this after generating tweets.",
    {"drafts": str},
)
async def save_drafts(args: dict[str, Any]) -> dict[str, Any]:
    """Save tweet drafts to drafts.json with timestamp."""
    try:
        drafts_text = args["drafts"]

        existing = []
        if os.path.exists(DRAFTS_FILE):
            with open(DRAFTS_FILE, "r") as f:
                existing = json.load(f)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "drafts": drafts_text,
        }
        existing.append(entry)

        with open(DRAFTS_FILE, "w") as f:
            json.dump(existing, f, indent=2)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Saved drafts to {DRAFTS_FILE} ({len(existing)} total entries)",
                }
            ]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error saving drafts: {e}"}],
            "is_error": True,
        }


@tool(
    "load_past_posts",
    "Load past tweets from past_posts.txt to match the user's writing style and tone.",
    {},
)
async def load_past_posts(args: dict[str, Any]) -> dict[str, Any]:
    """Read past posts for style matching."""
    try:
        if not os.path.exists(PAST_POSTS_FILE):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No past_posts.txt found. Will use default style.",
                    }
                ]
            }

        with open(PAST_POSTS_FILE, "r") as f:
            content = f.read()

        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Past posts for style reference:\n\n{content}",
                }
            ]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error loading past posts: {e}"}],
            "is_error": True,
        }


SYSTEM_PROMPT = """\
You are a Twitter/X post generator for designers, developers, and design engineers.

Your job: take a topic, project description, or design concept and generate 3-4 tweet variations.

## Tweet types to generate
1. Punchy/opinionated — a strong take that sparks conversation
2. Educational/tip-style — share a useful insight or technique
3. Conversational/relatable — something that resonates with the community
4. Engagement-optimized — a question or hot take that drives replies

## Rules
- Every tweet MUST be under 280 characters (this is critical, count carefully)
- Add 2-3 relevant hashtags per tweet (keep them natural, not spammy)
- Tone: authentic, casual, lowercase vibe when appropriate
- NEVER use these phrases: "game-changer", "unlock", "level up", "deep dive", \
"at the end of the day", "it's not about X it's about Y" (unless truly warranted)
- Avoid generic AI-sounding language. Write like a real person posting on twitter.
- No emojis unless they genuinely add something

## Workflow
1. FIRST: use load_past_posts to read the user's past tweets and match their voice/style
2. Optionally use WebSearch if the topic benefits from current trends or data
3. Generate the tweet variations
4. ALWAYS use save_drafts to save the generated tweets

## Format
Label each tweet with its type and number them. Show character count for each.
"""


async def main():
    posts_server = create_sdk_mcp_server(
        name="posts",
        version="1.0.0",
        tools=[save_drafts, load_past_posts],
    )

    options = ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"posts": posts_server},
        allowed_tools=[
            "mcp__posts__save_drafts",
            "mcp__posts__load_past_posts",
            "WebSearch",
            "WebFetch",
        ],
        permission_mode="acceptEdits",
        max_turns=15,
    )

    print("=" * 50)
    print("  Twitter/X Post Generator")
    print("  powered by Claude Agent SDK")
    print("=" * 50)
    print()
    print("Enter a topic, project description, or design")
    print("concept and get 3-4 tweet variations.")
    print("Type 'quit' to exit.")
    print()

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                topic = input("Topic: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nbye!")
                break

            if not topic:
                continue
            if topic.lower() in ("quit", "exit", "q"):
                print("bye!")
                break

            prompt = f"Generate tweet variations about: {topic}"

            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text)
                        elif isinstance(block, ToolUseBlock):
                            print(f"  [{block.name}]")

                elif isinstance(message, ResultMessage):
                    cost = message.total_cost_usd
                    if cost is not None:
                        print(f"\n  cost: ${cost:.4f}")
                    print()


if __name__ == "__main__":
    asyncio.run(main())
