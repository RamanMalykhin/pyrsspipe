PyRSSPipe is a simple and extendable CLI utility for building RSS feeds. It is built on top of [feedparser](https://github.com/kurtmckee/feedparser) and [rfeed](https://github.com/svpino/rfeed).



## Installation

1. Grab a release wheel from the releases page.
2. Install it with pip: `pip install pyrsspipe-<version>.whl`
3. Set `PYRSSPIPE_PIPECONFIG_DIR` and `PYRSSPIPE_LOG_DIR` environment variables to the directories where you want to store your pipeconfigs and the log of PyRSSPipe.

## Usage
PyRSSPipe is inspired by the "ETL" concept. In PyRSSPipe, "Extract" and "Load" phases for data that is supposed to make it into an RSS feed are handled by `input` and `output` modules. 
`input` modules are responsible for getting the data from whatever source. The "Transform" phase is universal and handled by the `makefeed` module, which creates an RSS feed from the data. `output` modules are responsible for writing that RSS feed to wherever. 
PyRSSPipe is quite agnostic to what `input` and `output` modules actually do under the hood. The only expectations are that:
-  `input` module must define a function called `get_feed_items` which returns a valid `feed_data` dict. 
- `output` module must define a function called `write_feed` which takes XML of the resulting RSS feed and does something with it (presumably, actually writes it somewhere).

PyRSSPipe is actually used with the help of JSON files called "pipeconfigs". A pipeconfig file defines what input and output modules are used for a single run of PyRSSPipe. It also defines the parameters that are passed to `get_feed_items` and `write_feed` functions in these modules respectively. In addition, it defines some parameters which are mandatory for any pipeconfig. It can be thought of in the same way as a DAG file in Apache Airflow.

After installation, PyRSSPipe exposes a CLI command `pyrsspipe`, which takes one and only one argument - the name of the pipeconfig file to run.

PyRSSPipe ships with some `input` and `output` modules that I built for my own use:
- `input` modules:
    - `archivelink` takes an existing RSS feed and replaces links to posts with cached versions of these links.
    - `dailybuffer` takes an existing RSS feed and creates a single feed item from all items in the feed that were published on the same day. This is useful for feeds that are based on chat-like applications (I use it for Telegram channels).
    - `discord` creates an RSS feed from a Discord channel, using Discord's REST API.
    - `patreon` creates an RSS feed from a Patreon creator's posts, using Patreon's  REST API.
- `output` modules:
    - `local` writes the resulting RSS feed to a local file.
    - `s3` writes the resulting RSS feed to an S3 bucket (or any other object storage compatible with `boto3`).

    ## Example
    Let's say you want to create an RSS feed from a Patreon creator, and you will put it on s3 (which is presumably accessible to your RSS reader somehow). 
    You would create a pipeconfig file like this:
    ```json
    {   
        "feed_name": "examplefeed_patreon",
        "feed_language": "en-us",
        "input": {
            "module": "patreon",
            "args": {
            "creator_name": "patreoncreator"
            }
        },
        "output": {
            "module": "s3",
            "args": {
                "s3_bucket": "mybucket",
                "s3_key": "creator_posts_feed.xml",
                "aws_access_key_id": "MY_AKEY",
                "aws_secret_access_key": "MY_SKEY",
                "endpoint_url": "https://s3.us-east-2.amazonaws.com",
                "acl": "public-read"
            }
        }
    }
    ```
    `feed_name` and `feed_language` are mandatory arguments for any pipeconfig, and are passed to `rfeed.Feed` under the hood. `input` and `output` keys define which modules out of pyrsspipe.input and pyrsspipe.output are used. `args` keys define the arguments that are passed to `get_feed_items` and `write_feed` in these modules as keyword arguments.

    You would save this into `PYRSSPIPE_PIPECONFIG_DIR` as `patreon_to_s3.json`, and then run `pyrsspipe --pipeconfig patreon_to_s3` in your terminal. 

    Assuming you would refresh the feed every day, you could then set up a cron job to run this command every day (or use any othe scheduling tool you prefer).