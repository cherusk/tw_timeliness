
import logging
import sys


def load_logger():
    from imp import reload
    reload(logging)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    return logging.getLogger(__name__)
