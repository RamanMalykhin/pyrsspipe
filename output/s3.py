import boto3

def write_feed(feed_xml, s3_bucket, s3_key, aws_access_key_id, aws_secret_access_key, endpoint_url, logger):
    if aws_access_key_id == '' and aws_secret_access_key == '' and endpoint_url == '':
        s3 = boto3.client('s3')
    else:
        s3 = boto3.client('s3')
    
    s3.Bucket(s3_bucket).put_object(Key=s3_key, Body=feed_xml, ContentType='application/xml')