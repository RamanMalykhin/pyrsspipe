def validate_feed_data(feed_data: dict):
    if not feed_data.get('feed_language'):
        raise ValueError('feed_data must contain language')
    if not feed_data.get('feed_name'):
        raise ValueError('feed_data must contain feed_name')
    if not feed_data.get('feed_filename'):
        raise ValueError('feed_data must contain feed_filename')
    if not feed_data.get('items_data'):
        raise ValueError('feed_data must contain items_data')
    for item_data in feed_data['items_data']:
        if not item_data.get('link'):
            raise ValueError('item_data must contain link')
        if not item_data.get('description'):
            raise ValueError('item_data must contain description')