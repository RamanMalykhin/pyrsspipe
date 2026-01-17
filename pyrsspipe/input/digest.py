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
        grouping = kwargs.get("grouping", "daily")  # Default to daily grouping

        input_feed = feedparser.parse(feed_link)

        # Parse the feed
        feed = feedparser.parse(feed_link)

        # Group posts based on the specified grouping
        grouped_posts = defaultdict(list)
        for entry in feed.entries:
            if 'published_parsed' in entry:
                published_date = datetime.date(
                    entry.published_parsed.tm_year,
                    entry.published_parsed.tm_mon,
                    entry.published_parsed.tm_mday,
                )

                if grouping == "weekly":
                    # Get the year and week number
                    year, week, _ = published_date.isocalendar()
                    group_key = f"{year}-W{week}"
                elif grouping == "monthly":
                    # Use year and month as the key
                    group_key = f"{published_date.year}-{published_date.month}"
                else:  # Default to daily
                    group_key = published_date

                grouped_posts[group_key].append(entry)

        # Sort posts within each group by timestamp, from latest to earliest
        for group in grouped_posts:
            grouped_posts[group].sort(key=lambda post: post.published_parsed, reverse=True)

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
        return output_feed

    @staticmethod
    def get_validator():
        class Validator(BaseModel):
            feed_link: str
            grouping: str = "daily"  # Default to daily
            include_summaries: bool = True  # Default to including summaries
        return Validator