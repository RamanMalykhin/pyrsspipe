import boto3

def write_feed(feed_xml, s3_bucket, s3_key, logger):
    s3 = boto3.client('s3')
    s3.Bucket(s3_bucket).put_object(Key=s3_key, Body=feed_xml, ContentType='application/xml')