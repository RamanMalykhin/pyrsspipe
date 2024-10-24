from bs4 import BeautifulSoup
import requests

def get_feed_items(page_url, article_items_xpath, item_title_xpath, item_content_xpath, item_url_xpath, debug_mode, logger):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    feed_items = []

    article_items = soup.select(article_items_xpath)
    for article in article_items:
        title = article.select_one(item_title_xpath).get_text()
        content = article.select_one(item_content_xpath).get_text()
        url = article.select_one(item_url_xpath).get('href')
        feed_item = {}
        feed_item["title"] = title
        feed_item["content"] = content
        feed_item["url"] = url
        feed_items.append(feed_item)

        if debug_mode:
            logger.debug(f"Scraped item: {feed_item}. Title: {title}. Content: {content}. Url: {url}")

    return feed_items
