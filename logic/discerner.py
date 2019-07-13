
import time
import logging
import datetime as dt


logger = logging.getLogger(__name__)

NOW = dt.datetime.now()
THRESH = CNFG ##


def is_exceeding(task):
    due_time = task['due']
    by = (NOW + THRESH) - due_time
    if by < 0:
        return True

    return False
