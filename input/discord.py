import requests
from discord_markdown.discord_markdown import convert_to_html
import os 
import contextlib

def get_feed_items(token, channel_id, guild_id, logger):

    discord_api_endpt = f'https://discord.com/api/channels/{channel_id}/messages?limit=20'
    auth_header = {'Authorization': f'Bot {token}'}

    logger.info(f'getting messages from {discord_api_endpt}')
    messages = requests.get(discord_api_endpt, headers=auth_header).json()
    logger.info(f'found {len(messages)} messages from {discord_api_endpt}')
    
    feed_items = []

    for message in messages:
        feed_item = {}
        message_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message['id']}"

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                message_content = convert_to_html(message['content'])

        feed_item['link'] = message_link
        feed_item['description'] = message_content
        feed_items.append(feed_item)
    
    return feed_items



