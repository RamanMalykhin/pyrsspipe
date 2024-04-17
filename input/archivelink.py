def get_feed_items(feed_link, which_archive, logger):
    import feedparser
    
    if which_archive == 'archive.today':
        substitute = 'https://archive.is/'
    elif which_archive == 'Wayback Machine':
        substitute = 'https://web.archive.org/web/'
    elif which_archive == 'Google Webcache':
        substitute = 'https://archive.today/'

    logger.info(f'parsing {feed_link}')
    ftfeed = feedparser.parse(feed_link)
    logger.info(f'found {len(ftfeed["entries"])} entries in {feed_link}')
    feed_items = []
    
    for entry in ftfeed['entries']:
        feed_item = {}
        feed_item['link'] = substitute + entry['link']
        feed_item['description'] = entry['summary']
        feed_item['title'] = entry['title']
        feed_items.append(feed_item)
    
    return feed_items