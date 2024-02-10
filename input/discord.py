import requests
import re

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
        message_content_with_fixed_links = re.sub("<(https?://\S+)>"," \n \g<1> \n ",message['content'])
        feed_item['link'] = message_link
        feed_item['description'] = message_content_with_fixed_links
        feed_items.append(feed_item)
    
    return feed_items



