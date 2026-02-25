import os
from typing import Any

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

from superserve import App

app = App(name="post-generator-agent")

PAST_POSTS_FILE = "past_posts.txt"


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
3. Generate the tweet variations and output them directly

## Format
Label each tweet with its type and number them. Show character count for each.
"""

posts_server = create_sdk_mcp_server(
    name="posts",
    version="1.0.0",
    tools=[load_past_posts],
)

options = ClaudeAgentOptions(
    system_prompt=SYSTEM_PROMPT,
    mcp_servers={"posts": posts_server},
    allowed_tools=[
        "mcp__posts__load_past_posts",
        "WebSearch",
        "WebFetch",
    ],
    permission_mode="acceptEdits",
    max_turns=15,
    include_partial_messages=True,
)


@app.session
async def main(session):
    async with ClaudeSDKClient(options=options) as client:
        async for topic, stream in session.turns():
            stream.status("Generating tweets...")

            await client.query(
                prompt=f"Generate tweet variations about: {topic}",
                session_id="chat",
            )

            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            stream.write(block.text)
                        elif isinstance(block, ToolUseBlock):
                            stream.status(f"Using {block.name}...")
                elif isinstance(msg, ResultMessage):
                    if msg.total_cost_usd is not None:
                        stream.metadata({"cost_usd": msg.total_cost_usd})


if __name__ == "__main__":
    app.run()
