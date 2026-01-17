import lxml.html
import requests
import logging
from pyrsspipe.input.base import AbstractInput
from rfeed import Item, Feed, Guid
from pydantic import BaseModel


class XPathInput(AbstractInput):
    @staticmethod
    def execute(logger: logging.Logger,**kwargs) -> Feed:
        debug_mode = kwargs["debug_mode"]
        page_url = kwargs["page_url"]
        article_items_xpath = kwargs["article_items_xpath"]
        item_title_xpath = kwargs["item_title_xpath"]
        item_content_xpath = kwargs["item_content_xpath"]
        item_url_xpath = kwargs["item_url_xpath"]

        debug_mode = bool(debug_mode)
        response = requests.get(page_url)
        tree = lxml.html.fromstring(response.content)
        tree.make_links_absolute(page_url)

        feed_items = []
        articles = tree.xpath(article_items_xpath)

        if debug_mode:
            logger.setLevel(logging.DEBUG)

        logger.debug(f"Scraped {len(articles)} items from {page_url}")

        for article in articles:
            logger.debug(f"processing {article}")

            title = str(article.xpath(item_title_xpath)[0])
            logger.debug(f"found title: {title}")
            content = str(article.xpath(item_content_xpath)[0])
            logger.debug(f"found content: {content}")
            url = str(article.xpath(item_url_xpath)[0])
            logger.debug(f"found url: {url}")

            feed_item = Item(
                title=title,
                link=url,
                description=content,
                author="placeholder",
                guid=Guid(url),
            )

            feed_items.append(feed_item)

        feed = Feed(
            title="Feed",
            link=page_url,
            description="",
            language="en-US",
            items=feed_items,
        )

        if debug_mode:
            logger.setLevel(logging.INFO)

        return feed

    @staticmethod
    def get_validator():
        class Validator(BaseModel):
            debug_mode: bool
            page_url: str
            article_items_xpath: str
            item_title_xpath: str
            item_content_xpath: str
            item_url_xpath: str

            class Config:
                json_schema_extra = {
                    "example": {
                        "debug_mode": False,
                        "page_url": "https://example.com",
                        "article_items_xpath": "//xpath/to/articles",
                        "item_title_xpath": "./relative/xpath/to/title",
                        "item_content_xpath": "./relative/xpath/to/content",
                        "item_url_xpath": "./relative/xpath/to/url"
                    }
                }
        return Validator
