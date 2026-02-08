import datetime
import logging
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
        grouping = kwargs.get("grouping", "daily")  # Default to daily grouping


        if kwargs['debug_mode']:
            logger.setLevel(logging.DEBUG)

        logger.debug("DailyDigestInput.execute(feed_link=%s, grouping=%s)", feed_link, grouping)

        input_feed = feedparser.parse(feed_link)

        # Parse the feed
        feed = feedparser.parse(feed_link)
        logger.debug("Fetched %d entries from feed", len(feed.entries))

        def build_group_key(date_obj):
            if grouping == "weekly":
                year, week, _ = date_obj.isocalendar()
                return f"{year}-W{week}"
            if grouping == "monthly":
                return f"{date_obj.year}-{date_obj.month}"
            return date_obj

        current_period_key = build_group_key(datetime.date.today())
        logger.debug("Current %s period key resolved to %s", grouping, current_period_key)

        # Group posts based on the specified grouping
        grouped_posts = defaultdict(list)
        for entry in feed.entries:
            if 'published_parsed' in entry:
                published_date = datetime.date(
                    entry.published_parsed.tm_year,
                    entry.published_parsed.tm_mon,
                    entry.published_parsed.tm_mday,
                )
                group_key = build_group_key(published_date)
                if group_key == current_period_key:
                    logger.debug("Skipping entry %s because it belongs to current %s period", entry.get('id', entry.get('link', 'unknown')), grouping)
                    continue
                grouped_posts[group_key].append(entry)
                logger.debug("Added entry %s to group %s", entry.get('id', entry.get('link', 'unknown')), group_key)

        # Sort posts within each group by timestamp, from latest to earliest
        for group in grouped_posts:
            grouped_posts[group].sort(key=lambda post: post.published_parsed, reverse=True)
            logger.debug("Group %s has %d posts after sorting", group, len(grouped_posts[group]))

        html_descriptions = {}
        include_summaries = kwargs.get("include_summaries", True)  # Default to including summaries

        # Include summaries in the grouped HTML content
        for group, posts in grouped_posts.items():
            html_content = f"<h2>Posts for {group}</h2><ul>"
            for post in posts:
                author = post.get("author", "unknown@example.org")
                title = post.get("title", "No Title")
                link = post.get("link", "#")
                published = post.get("published", "Unknown Date")
                summary = post.get("summary_detail", {}).get("value", "No Summary")
                html_content += (
                    f"<li><strong>{title}</strong> by {author} (<a href='{link}'>link</a>) - Published: {published}"
                )
                if include_summaries:
                    html_content += f"<br><em>Summary:</em> {summary}"
                html_content += "</li>"
            html_content += "</ul>"
            html_descriptions[group] = html_content
            logger.debug("Built HTML description for group %s", group)

        feed_items = []
        for group, html_content in html_descriptions.items():
            feed_items.append(
                Item(
                    title=f"{grouping.capitalize()} Digest for {group}",
                    description=html_content,
                    link=feed_link,
                    guid=Guid(f"{feed_link}#{group}"),
                    author='unknown@example.org'))
        output_feed = Feed(
            title=f"{grouping.capitalize()} Digest Feed: {input_feed.feed.title}",
            link=feed_link,
            description=f"{grouping.capitalize()} Digest Feed generated from {input_feed.feed.title}",
            language=input_feed.feed.get("language", "en-US"),
            items=feed_items,
        )
        logger.debug("Constructed digest feed with %d grouped items", len(feed_items))
        return output_feed

    @staticmethod
    def get_validator():
        class Validator(BaseModel):
            feed_link: str
            grouping: str = "daily"  # Default to daily
            include_summaries: bool = True  # Default to including summaries
            debug_mode: bool  # Default to non-debug mode

            class Config:
                json_schema_extra = {
                    "example": {
                        "feed_link": "https://example.com/rss",
                        "grouping": "daily",
                        "include_summaries": True,
                        "debug_mode": False
                    }
                }
        return Validator