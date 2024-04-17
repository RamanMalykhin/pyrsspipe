import re

import requests


def get_feed_items(creator_name, logger):
    logger.info(f'starting pull for {creator_name}')

    url = f'https://www.patreon.com/{creator_name}'
    api_url = 'https://www.patreon.com/api/posts'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url
    }
    posts_data = []
    with requests.session() as s:
        logger.info(f'getting campaign id for {creator_name}')
        html_text = s.get(url, headers=headers).text
        campaign_id = re.search(r'https://www\.patreon\.com/api/campaigns/(\d+)', html_text).group(1)
        logger.info(f'campaign id for {creator_name} is {campaign_id}')
        logger.info(f'getting posts for {creator_name}')
        data = s.get(api_url, headers=headers, params={'filter[campaign_id]': campaign_id, 'filter[contains_exclusive_posts]': 'true', 'sort': '-published_at'}).json()
        logger.info(f'found {len(data["data"])} posts for {creator_name}')
        for d in data['data']:
            post_data = {
                'title': d['attributes']['title'],
                'link': f"https://www.patreon.com/{d['attributes']['patreon_url']}",
                'description': d['attributes']['teaser_text'],
                'author': 'placeholder@example.py'
            }
            posts_data.append(post_data)

    logger.info(f'finished pull for {creator_name}')
    return posts_data