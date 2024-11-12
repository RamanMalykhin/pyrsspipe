import contextlib
import os
import requests
from discord_markdown.discord_markdown import convert_to_html
from pyrsspipe.input.base import AbstractInput
from rfeed import Item, Feed, Guid
import dateutil.parser
from datetime import datetime
from logging import Logger


class DiscordInput(AbstractInput):
    def execute(
        token: str, channel_id: int, guild_id: int, title: str, logger: Logger
    ) -> Feed:
        discord_api_endpt = (
            f"https://discord.com/api/channels/{channel_id}/messages?limit=20"
        )
        auth_header = {"Authorization": f"Bot {token}"}

        logger.info(f"getting messages from {discord_api_endpt}")
        messages = requests.get(discord_api_endpt, headers=auth_header).json()
        logger.info(f"found {len(messages)} messages from {discord_api_endpt}")

        feed_items = []

        for message in messages:
            message_link = (
                f"https://discord.com/channels/{guild_id}/{channel_id}/{message['id']}"
            )

            with open(os.devnull, "w") as devnull:
                with contextlib.redirect_stdout(devnull):
                    message_content = convert_to_html(message["content"])

            feed_items.append(
                Item(
                    title=f"{message_content[:50]}...",
                    link=message_link,
                    description=message_content,
                    author=message["author"]["username"],
                    guid=Guid(message_link),
                    pubDate=dateutil.parser.parse(message["timestamp"]),
                )
            )

        feed = Feed(
            title=title,
            link=discord_api_endpt,
            description="",
            language="en-US",
            lastBuildDate=datetime.datetime.today(),
            items=feed_items,
        )

        return feed
