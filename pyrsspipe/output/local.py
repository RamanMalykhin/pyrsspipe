import os
from pyrsspipe.output.base import AbstractOutput
from logging import Logger
from rfeed import Feed

class LocalOutput(AbstractOutput):
    @staticmethod
    def execute(logger: Logger, feed: Feed, **kwargs) -> None:
        output_dir = kwargs["output_dir"]
        file_name = kwargs["file_name"]

        p = os.path.join(output_dir, file_name)
        logger.info(f"writing feed to {p}")

        with open(os.path.join(output_dir, file_name), encoding="utf8", mode="w") as f:
            f.write(feed.rss())

    @staticmethod
    def get_validator():
        from pydantic import BaseModel
        from pydantic import DirectoryPath

        class LocalOutputModel(BaseModel):
            output_dir: DirectoryPath
            file_name: str

        return LocalOutputModel
