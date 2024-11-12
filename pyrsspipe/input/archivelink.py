import feedparser
from pyrsspipe.input.base import AbstractInput
from rfeed import Item, Feed
from datetime import datetime
from logging import Logger
from typing import Literal


class ArchiveLinkInput(AbstractInput):
    def execute(
        logger: Logger,
        feed_link: str,
        which_archive: Literal["archive.today", "Wayback Machine"],
    ) -> Feed:
        if which_archive == "archive.today":
            prefix = "https://archive.is/"
        elif which_archive == "Wayback Machine":
            prefix = "https://web.archive.org/web/"

        logger.info(f"parsing {feed_link}")
        feed = feedparser.parse(feed_link)
        logger.info(f'found {len(feed["entries"])} entries in {feed_link}')
        feed_items = []

        for entry in feed["entries"]:
            feed_items.append(
                Item(
                    title=entry["title"],
                    link=prefix + entry["link"],
                    description=entry["summary"],
                    author=entry["author"],
                    guid=entry["id"],
                )
            )

        feed = Feed(
            title=feed.title,
            link=feed_link,
            description="",
            language=feed.language,
            lastBuildDate=datetime.datetime.today(),
            items=feed_items,
        )

        return feed
