
import collections
import itertools as it
from taskw import TaskWarrior
from introspection import load_logger


logger = load_logger()


class Collector(collections.Iterable):

    def __init__(self, cnfg):
        self._tasks = list()

        tw = TaskWarrior(config_filename=cnfg['core']['taskrc'])
        all_tasks = tw.load_tasks()

        selected_tasks = it.chain([all_tasks[category]
                                   for category in
                                   ['pending', 'waiting']
                                   if category in all_tasks.keys()])
        for t in selected_tasks:
            logger.debug("loaded Task>> {0}:".format(str(t)))
            self._tasks.append(t)

    def __iter__(self):
        #  wrap as iterator
        return it.chain(self._tasks)
