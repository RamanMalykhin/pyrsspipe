def write_feed(feed_xml, feed_file_path):
    with open(feed_file_path, 'w') as f:
        f.write(feed_xml)