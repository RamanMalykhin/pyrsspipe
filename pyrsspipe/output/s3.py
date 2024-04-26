import boto3


def write_feed(
    feed_xml,
    s3_bucket,
    s3_key,
    aws_access_key_id,
    aws_secret_access_key,
    endpoint_url,
    acl,
    logger,
):
    if aws_access_key_id == "" and aws_secret_access_key == "" and endpoint_url == "":
        s3 = boto3.client("s3")
    else:

        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
        )

    response = s3.put_object(
        Key=s3_key, Body=feed_xml, Bucket=s3_bucket, ContentType="application/xml", ACL = acl

    )
    logger.info(f"boto3 put_object success. response: {response}")
    logger.info(f"written feed to s3://{s3_bucket}/{s3_key}")

