import os
import subprocess
from logging import getLogger

LOG = getLogger(__name__)
PROJ_NAME = os.environ["PROJ_NAME"]


def run(cmd, exit_on_error=True, *args, **kwargs):
    LOG.info(cmd, flush=True)
    if exit_on_error:
        kwargs.update({"check": True})
    try:
        return subprocess.run(cmd, *args, **kwargs)
    except subprocess.CalledProcessError as error:
        if exit_on_error:
            exit(str(error))
        else:
            raise
