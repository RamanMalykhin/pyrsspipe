import feedparser
import datetime


def get_feed_items(input_feed_link, s3_url):
    input_feed = feedparser.parse(input_feed_link)
    feed_entries = input_feed['entries']
    feed_entries.reverse()

    dateagg_dict = {}
    output_feed_entries = []

    for entry in feed_entries:
        publish_date = entry['published_parsed']
        agg_date = str(datetime.date(publish_date.tm_year, publish_date.tm_mon, publish_date.tm_mday))
        
        entry_content = entry['summary_detail']['value']
        
        dateagg_dict.setdefault(agg_date, []).append(entry_content)

    output_feed_data = []
    for agg_date, entries in dateagg_dict.items():
        output_feed_item = {}
        title = agg_date+'.html'

        aggregated_entries_html = "<html>" + \
                " <head> <meta charset = \"UTF-8\">" + \
                "<title>" + agg_date+ "</title>" + \
                "</head> <body>" + \
                "<hr>".join(entries) + \
                "</body> </html>"
        
        description = aggregated_entries_html[0:200]+'...'
        key =  agg_date+'.html'
        link = s3_url + key

        output_feed_item['title'] = agg_date
        output_feed_item['description'] = description
        output_feed_item['actual_item_content'] = {'key': key, 'html_content': aggregated_entries_html}
        output_feed_item['link'] = link

        output_feed_entries.append(output_feed_item)