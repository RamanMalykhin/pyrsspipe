import boto3
from pyrsspipe.output.base import AbstractOutput
from logging import Logger
from rfeed import Feed

class S3Output(AbstractOutput):

    @staticmethod
    def execute(
        logger: Logger,
        feed: Feed,
        **kwargs,
    ) -> None:
        s3_bucket = kwargs["s3_bucket"]
        s3_key = kwargs["s3_key"]
        acl = kwargs["acl"]
        aws_access_key_id = kwargs["aws_access_key_id"]
        aws_secret_access_key = kwargs["aws_secret_access_key"]
        endpoint_url = kwargs["endpoint_url"]

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
            Key=s3_key,
            Body=feed.rss(),
            Bucket=s3_bucket,
            ContentType="application/xml",
            ACL=acl,
        )
        logger.info(f"boto3 put_object success. response: {response}")
        logger.info(f"written feed to s3://{s3_bucket}/{s3_key}")


    @staticmethod
    def get_validator():
        from pydantic import BaseModel
        from pydantic import AnyUrl

        class S3OutputModel(BaseModel):
            s3_bucket: str
            s3_key: str
            acl: str
            aws_access_key_id: str
            aws_secret_access_key: str
            endpoint_url: AnyUrl

        return S3OutputModel