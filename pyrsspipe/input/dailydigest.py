import datetime
from logging import Logger
import feedparser
from rfeed import Feed, Item, Guid
from pyrsspipe.input.base import AbstractInput
from pydantic import BaseModel
from collections import defaultdict

class DailyDigestInput(AbstractInput):
    @staticmethod
    def execute(logger: Logger, **kwargs) -> Feed:
        feed_link = kwargs["feed_link"]

        input_feed = feedparser.parse(feed_link)

        # Parse the feed
        feed = feedparser.parse('https://krytykapolityczna.pl/feed/')

        # Group posts by day
        grouped_posts = defaultdict(list)
        for entry in feed.entries:
            if 'published_parsed' in entry:
                # Convert published timestamp to date
                published_date = datetime.date(
                    entry.published_parsed.tm_year,
                    entry.published_parsed.tm_mon,
                    entry.published_parsed.tm_mday,
                )
                grouped_posts[published_date].append(entry)

        # Sort posts within each date by timestamp, from latest to earliest
        for date in grouped_posts:
            grouped_posts[date].sort(key=lambda post: post.published_parsed, reverse=True)

        html_descriptions = {}
        for date, posts in grouped_posts.items():
            html_content = f"<h2>Posts for {date}</h2><ul>"
            for post in posts:
                author = post.get("author", "unknown@example.org")
                title = post.get("title", "No Title")
                link = post.get("link", "#")
                published = post.get("published", "Unknown Date")
                html_content += f"<li><strong>{title}</strong> by {author} (<a href='{link}'>link</a>) - Published: {published}</li>"
            html_content += "</ul>"
            html_descriptions[date] = html_content

        feed_items = []
        for date, html_content in html_descriptions.items():
            feed_items.append(
                Item(
                    title=f"Daily Digest for {date}",
                    description=html_content,
                    link=feed_link,
                    guid=Guid(f"{feed_link}#{date}"),
                    author='unknown@example.org'))
        output_feed = Feed(
            title=f"Daily Digest Feed: {input_feed.feed.title}",
            link=feed_link,
            description=f"Daily Digest Feed generated from {input_feed.feed.title}",
            language=input_feed.feed.get("language", "en-US"),
            items=feed_items,
        )
        return output_feed

    @staticmethod
    def get_validator():
        class Validator(BaseModel):
            feed_link: str
        return Validator