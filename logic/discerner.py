
import core
import datetime as dt
from introspection import load_logger

logger = load_logger()

NOW = dt.datetime.now()
THRESH = None

TASK_DATE_FMT = '%Y%m%dT%H%M%SZ'


def is_becoming_due(task):
    due_time = dt.datetime.strptime(task['due'],
                                    TASK_DATE_FMT)
    by = (NOW + dt.timedelta(**THRESH)) - due_time
    if by.total_seconds() < 0:
        return True

    return False


def is_becoming_startable(task):
    start_time = dt.datetime.strptime(task['scheduled'],
                                      TASK_DATE_FMT)
    by = (NOW + dt.timedelta(**THRESH)) - start_time
    if by.total_seconds() < 0:
        return True

    return False


def categorize(task):
    categories = []
    for category, mechanism in [('dueing', is_becoming_due),
                                ('starting', is_becoming_startable)]:
        if mechanism(task):
            categories.append[category]

    return categories
