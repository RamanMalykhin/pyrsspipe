import feedparser
import datetime


def get_feed_items(input_feed_link):
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

    for agg_date, entries in dateagg_dict.items():
        output_feed_item = {}
        aggregated_entries_html = "<html>" + \
                " <head> <meta charset = \"UTF-8\">" + \
                "<title>" + agg_date+ "</title>" + \
                "</head> <body>" + \
                "<hr>".join(entries) + \
                "</body> </html>"
        
        link = input_feed_link

        output_feed_item['title'] = agg_date
        output_feed_item['description'] = aggregated_entries_html
        output_feed_item['link'] = link

        output_feed_entries.append(output_feed_item)
    
    return output_feed_entries