import datetime
from logging import Logger
import feedparser
from rfeed import Feed, Item, Guid
from pyrsspipe.input.base import AbstractInput


class DailyBufferInput(AbstractInput):
    def execute(feed_link: str, logger: Logger) -> Feed:
        input_feed = feedparser.parse(feed_link)
        feed_entries = input_feed["entries"]
        feed_entries.reverse()

        dateagg_dict = {}
        output_feed_entries = []

        for entry in feed_entries:
            publish_date = entry["published_parsed"]
            agg_date = str(
                datetime.date(
                    publish_date.tm_year, publish_date.tm_mon, publish_date.tm_mday
                )
            )

            entry_content = entry["summary_detail"]["value"]
            entry_link = entry["link"]

            dateagg_dict.setdefault(agg_date, []).append((entry_content, entry_link))

        for agg_date, entries in dateagg_dict.items():
            all_entry_contents, all_entry_links = map(list, zip(*entries))

            output_feed_item = {}
            aggregated_entries_html = (
                "<html>"
                + ' <head> <meta charset = "UTF-8">'
                + "<title>"
                + agg_date
                + "</title>"
                + "</head> <body>"
                + "<hr>".join(all_entry_contents)
                + "</body> </html>"
            )

            first_entry_in_aggregate_link = all_entry_links[0]

            output_feed_item = Item(
                title=agg_date,
                description=aggregated_entries_html,
                link=first_entry_in_aggregate_link,
                guid=Guid(first_entry_in_aggregate_link),
                author="placeholder@example.org",
            )

            output_feed_entries.append(output_feed_item)

        feed = Feed(
            title=input_feed["feed"]["title"],
            link=feed_link,
            description="",
            language=input_feed["feed"]["language"],
            lastBuildDate=datetime.datetime.today(),
            items=output_feed_entries,
        )

        return feed
