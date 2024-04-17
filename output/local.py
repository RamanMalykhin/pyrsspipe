import os

def write_feed(feed_xml, output_dir, file_name, logger):
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(feed_xml)