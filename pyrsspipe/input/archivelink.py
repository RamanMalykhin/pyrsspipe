import feedparser
from pyrsspipe.input.base import AbstractInput
from rfeed import Item, Feed, Guid
from datetime import datetime
from logging import Logger
from pydantic import BaseModel


class ArchiveLinkInput(AbstractInput):
    @staticmethod
    def execute(
        logger: Logger,
        **kwargs    ) -> Feed:
        which_archive = kwargs["which_archive"]
        feed_link = kwargs["feed_link"]


        if which_archive == "archive.today":
            prefix = "https://archive.is/"
        elif which_archive == "Wayback Machine":
            prefix = "https://web.archive.org/web/"
        else:
            raise ValueError(f"Unknown or unsupported archive service: {which_archive}")

        logger.info(f"parsing {feed_link}")
        ingested_feed = feedparser.parse(feed_link)
        logger.info(f'found {len(ingested_feed["entries"])} entries in {feed_link}')
        feed_items = []

        for entry in ingested_feed["entries"]:
            feed_items.append(
                Item(
                    title=entry["title"],
                    link=prefix + entry["link"],
                    description=entry["summary"],
                    author="placeholder@example.com",
                    guid=Guid(prefix + entry["link"]),
                )
            )

        feed = Feed(
            title=ingested_feed.feed.title,
            link=feed_link,
            description=ingested_feed.feed.title_detail.value,
            language=ingested_feed.feed.language,
            lastBuildDate=datetime.today(),
            items=feed_items,
        )

        return feed

    @staticmethod
    def get_validator():
        class Validator(BaseModel):
            which_archive: str
            feed_link: str
        return Validator