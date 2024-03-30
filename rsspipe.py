import json
import argparse
import logging
import logging
from importlib import import_module

from validation import validate_feed_data
from makefeed import make_feed_wrapper
import os

# Initialize logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',  handlers=[
    logging.FileHandler("debug.log"),
    logging.StreamHandler()
])

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Specify the config name')
    args = parser.parse_args()
    config_name = args.config
    logging.info(f'using config {config_name}')

    # Open the config file
    
    config_path = os.path.join(os.path.dirname(__file__), f"configs/{config_name}.json")
    with open(config_path, 'r') as file:
        config = json.load(file)
    logging.info(f'parsed config {config_name}')

    in_module = config['in']['module']
    in_module = import_module(f"input.{in_module}")
    in_function = getattr(in_module, 'get_feed_items')
        
    logging.info(f'imported in module {in_module}, using in function {in_function}')

    feed_items = in_function(**config['in']['args'], logger=logging)

    feed_data = {
        'feed_name': config['feed_name'],
        'feed_filename': config['feed_filename'],
        'feed_language': config['feed_language'],
        'items_data': feed_items
    }

    try:
        validate_feed_data(feed_data)
    except ValueError as e:
        logging.error(f'invalid feed_data: {e}')
        raise e
    
    feed_xml = make_feed_wrapper(feed_data)
    logging.info('feed_xml created')

    out_module = config['out']['module']
    out_module = import_module(f"output.{out_module}")
    out_function = getattr(out_module, 'write_feed')
    logging.info(f'imported out module {out_module}, using out function {out_function}')

    out_function(feed_xml, **config['out']['args'], logger=logging)
    logging.info('output complete')
    
    logging.info('pyrsspipe complete') 

except Exception as e:
    logging.error(e)
    raise e



