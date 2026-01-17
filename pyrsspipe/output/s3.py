import boto3
from pyrsspipe.output.base import AbstractOutput
from logging import Logger
from rfeed import Feed
import os

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
        aws_access_key_id = os.getenv(kwargs["aws_access_key_id_env_var"])
        aws_secret_access_key = os.getenv(kwargs["aws_secret_access_key_env_var"])
        endpoint_url = os.getenv(kwargs["endpoint_url_env_var"])

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
            aws_access_key_id_env_var: str
            aws_secret_access_key_env_var: str
            endpoint_url_env_var: AnyUrl

            class Config:
                json_schema_extra = {
                    "example": {
                        "s3_bucket": "example-bucket",
                        "s3_key": "path/to/feed.xml",
                        "acl": "public-read",
                        "aws_access_key_id_env_var": "AWS_ACCESS_KEY_ID_ENV_VAR_NAME",
                        "aws_secret_access_key_env_var": "AWS_SECRET_ACCESS_KEY_ENV_VAR_NAME",
                        "endpoint_url_env_var": "https://s3.example.com"
                    }
                }

        return S3OutputModel