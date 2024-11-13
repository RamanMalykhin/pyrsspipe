import os
from pyrsspipe.output.base import AbstractOutput

class LocalOutput(AbstractOutput):
    def execute(feed_xml: str, output_dir: str, file_name: str, logger) -> None:
            with open(os.path.join(output_dir, file_name), encoding="utf8", mode="w") as f:
                f.write(feed_xml)
