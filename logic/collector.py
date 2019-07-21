
import collections
import itertools as it
import logging
from taskw import TaskWarrior


logger = logging.getLogger(__name__)


class Collector(collections.Iterable):

    def __init__(self, cnfg):
        self._tasks = list()

        tw = TaskWarrior(config_filename=cnfg['core']['taskrc'])
        all_tasks = tw.load_tasks()

        selected_tasks = it.chain([all_tasks[category]
                                   for category in
                                   ['pending', 'waiting']])
        for t in selected_tasks:
            logger.debug("loaded Task>> {0}:".format(str(t)))
            self._tasks.append(t)

    def __iter__(self):
        #  wrap as iterator
        return it.chain(self._tasks)
