import datetime

import rfeed


def _make_rfeed_item(link, description, author=None, title=None):
    if not author:
        author = "placeholder@example.com"
    if not title:
        title = description[:50]

    item = rfeed.Item(
        title=title,
        link=link,
        description=description,
        author=author,
        guid=rfeed.Guid(link),
    )
    return item


def _make_rfeed_feed(feed_items, feed_link, feed_name, feed_language):

    # create feed with passed items
    feed = rfeed.Feed(
        title=feed_name,
        link=feed_link,
        description="",
        language=feed_language,
        lastBuildDate=datetime.datetime.today(),
        items=feed_items,
    )

    return feed


def make_feed_wrapper(feed_data, feed_link=None):
    if not feed_link:
        feed_link = "http://example.com"
    feed_data_items = feed_data["items_data"]

    feed_items = []
    for feed_data_item in feed_data_items:
        feed_item = _make_rfeed_item(
            feed_data_item["link"],
            feed_data_item["description"],
            author=feed_data_item.get("author"),
            title=feed_data_item.get("title"),
        )
        feed_items.append(feed_item)

    feed = _make_rfeed_feed(
        feed_items=feed_items,
        feed_link=feed_link,
        feed_name=feed_data["feed_name"],
        feed_language=feed_data["feed_language"],
    )

    feed_xml = feed.rss()

    return feed_xml
