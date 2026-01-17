import argparse
import json
import logging
import os

from pyrsspipe.validation import ConfigModel


def pyrsspipe():
    pipeconfig_dir = os.getenv("PYRSSPIPE_PIPECONFIG_DIR")
    log_dir = os.getenv("PYRSSPIPE_LOG_DIR")

    if not pipeconfig_dir or not log_dir:
        raise EnvironmentError(
            "Environment variables PYRSSPIPE_PIPECONFIG_DIR and PYRSSPIPE_LOG_DIR must be set."
            f"As of now, PYRSSPIPE_PIPECONFIG_DIR is '{pipeconfig_dir}', and PYRSSPIPE_LOG_DIR is '{log_dir}'"
        )

    # Initialize logger
    logging.basicConfig(
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "pyrsspipe.log")),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger()

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--pipeconfig", help="Specify the pipeconfig name", required=True
        )
        args = parser.parse_args()
        pipeconfig_name = args.pipeconfig
        logger.info(f"using pipeconfig {pipeconfig_name}")

        # Open the pipeconfig file

        pipeconfig_path = f"{pipeconfig_dir}/{pipeconfig_name}.json"
        with open(pipeconfig_path, "r") as file:
            pipeconfig_raw = json.load(file)
            pipeconfig = ConfigModel(**pipeconfig_raw)

        logger.info(f"parsed pipeconfig {pipeconfig_name}")
        logger.info(
            f"Using input module {pipeconfig.input.module_name}, output module {pipeconfig.output.module_name}"
        )

        feed = pipeconfig.input.execute(logger, **pipeconfig.input.args)

        logger.info("feed created")
        pipeconfig.output.execute(logger, feed, **pipeconfig.output.args)

        logger.info("output complete")

        logger.info("pyrsspipe complete")

    except Exception as e:
        logger.error(e)
        raise e
