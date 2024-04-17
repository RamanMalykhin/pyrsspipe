import feedparser


def get_feed_items(feed_link, which_archive, logger):
    
    if which_archive == 'archive.today':
        substitute = 'https://archive.is/'
    elif which_archive == 'Wayback Machine':
        substitute = 'https://web.archive.org/web/'
    elif which_archive == 'Google Webcache':
        substitute = 'https://webcache.googleusercontent.com/search?q=cache:'

    logger.info(f'parsing {feed_link}')
    feed = feedparser.parse(feed_link)
    logger.info(f'found {len(feed["entries"])} entries in {feed_link}')
    feed_items = []
    
    for entry in feed['entries']:
        feed_item = {}
        feed_item['link'] = substitute + entry['link']
        feed_item['description'] = entry['summary']
        feed_item['title'] = entry['title']
        feed_items.append(feed_item)
    
    return feed_items