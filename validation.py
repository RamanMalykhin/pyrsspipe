def validate_feed_data(feed_data, uploadable_feed_items=None):
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
        if uploadable_feed_items:
             if not item_data.get('actual_item_content'):
                 raise ValueError(f'feed is supposed to provide actual_item_content, but none found in item {item_data}')
             else:
                 if not item_data['actual_item_content'].get('key'):
                     raise ValueError(f'actual_item_content must contain key in item {item_data}')
                 if not item_data['actual_item_content'].get('html_content'):
                     raise ValueError(f'actual_item_content must contain html_content in item {item_data}')