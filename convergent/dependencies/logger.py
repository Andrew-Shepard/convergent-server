import logging

__all__ = ["logger"]

logging.basicConfig(
    format="%(asctime)s|%(name)s|%(levelname)-5.5s|%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("convergent")
logger.setLevel("INFO")
