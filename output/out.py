import rfeed
import datetime
import boto3


def _make_rfeed_item(link, description, author=None, title=None):
        if not author:
                 author='placeholder@example.com'
        if not title:
            title = description[:50]

        item = rfeed.Item(
            title=title,
            link=link,
            description=description,
            author=author,
            guid=rfeed.Guid(link)
        )
        return item

def _make_rfeed_feed(feed_items, feed_link, feed_name, feed_language):

    # create feed with passed items
    feed = rfeed.Feed(
        title=feed_name,
        link=feed_link,
        description='',
        language=feed_language,
        lastBuildDate=datetime.datetime.today(),
        items=feed_items)

    return feed


def _make_feed_wrapper(feed_data, output_feed_link):
        feed_data_items = feed_data['items_data']
        
        feed_items = []
        for feed_data_item in feed_data_items:
            feed_item = _make_rfeed_item(feed_data_item['link'], feed_data_item['description'], author=feed_data_item.get('author'), title=feed_data_item.get('title'))
            feed_items.append(feed_item)

        feed = _make_rfeed_feed(feed_items=feed_items, feed_link=output_feed_link, feed_name=feed_data['feed_name'], feed_language=feed_data['feed_language'])
        
        feed_xml = feed.rss()

        return feed_xml

def _write_feed_to_s3(feed_xml, s3_bucket, s3_key):
    s3 = boto3.client('s3')
    s3.Bucket(s3_bucket).put_object(Key=s3_key, Body=feed_xml, ContentType='application/xml')

def _write_feed_to_file(feed_xml, file_path):
    with open(file_path, 'w') as f:
        f.write(feed_xml)

def _write_feed_wrapper_singlefile(feed_xml, s3_bucket=None, s3_key=None, file_path=None):
    if s3_bucket and s3_key:
        _write_feed_to_s3(feed_xml, s3_bucket, s3_key)
    elif file_path:
        _write_feed_to_file(feed_xml, file_path)
    else:
        raise ValueError('Must specify either s3_bucket and s3_key or file_path')

def _validate_feed_data(feed_data, uploadable_feed_items=None):
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
        
def out_wrapper(feed_data, logger, output_feed_link=None,s3_bucket=None, file_path=None, uploadable_feed_items=False):
    logger.info('starting output')
    try:
        _validate_feed_data(feed_data)
    except ValueError as e:
        logger.error(f'invalid feed_data: {e}')
        raise e
    
    if not output_feed_link:
        output_feed_link = 'http://example.com/'

    logger.info(f'feed_data is valid, making feed {feed_data["feed_name"]}')

    feed_xml = _make_feed_wrapper(feed_data, output_feed_link)
    logger.info(f'feed {feed_data["feed_name"]} created')
    
    logger.info('writing feed')
    _write_feed_wrapper_singlefile(feed_xml, s3_bucket=s3_bucket, s3_key=feed_data["feed_filename"], file_path=file_path)
    logger.info('feed written')

    if uploadable_feed_items:
        logger.info('writing actual_item_content')
        for item_data in feed_data['items_data']:
            logger.info(f'writing actual_item_content for {item_data["link"]}')
            _write_feed_wrapper_singlefile(item_data['actual_item_content']['html_content'], s3_bucket=s3_bucket, s3_key=item_data['actual_item_content']['key'])
        logger.info('actual_item_content written')
    logger.info(f'output complete with parameters: s3_bucket: {s3_bucket}, file_path: {file_path}')  