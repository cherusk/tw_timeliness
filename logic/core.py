
import daemon
from timeloop import Timeloop
from datetime import timedelta
from collector import Collector
import  discerner
from communication import Notifier
import argparse
import os
import sys
import logging
import yaml


logger = logging.getLogger(__name__)


TL = Timeloop()
INTERVAL = 60


class Cnfg:

    def __init__(self, file=None):
        pass

    def _load(self, _file, logic=None):
        with open(_file, "r") as fp:
            return logic(fp)

    def provide(self, param_file=None):
        run_cnfg = self._load(param_file,
                              logic=yaml.load)
        return run_cnfg

CNFG = dict(interval=INTERVAL)


@TL.job(interval=timedelta(seconds=CNFG['interval']))
def run():
    global CNFG

    discerner.THRESH = CNFG['reporting']['threshold']
    notifier = Notifier(CNFG)
    for task in Collector(CNFG):
        logger.debug("categorized Tasks>>")
        categories = discerner.categorize(task)
        logger.debug("--> {0} - Categories {1}".format(str(task),
                                                       categories))
        notifier.gather(task, categories)

    notifier.release()


def start(args, oneshot=False):
    global CNFG

    CNFG = Cnfg(args.cnfg).provide()

    if not oneshot:
        with daemon.DaemonContext() as context:
            TL.start(block=True)
