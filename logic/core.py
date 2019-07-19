
import daemon
from timeloop import Timeloop
from datetime import timedelta
from collector import Collector
from . import discerner
from . import Notifier
import argparse
import os
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


def form_args():
    parser = argparse.ArgumentParser(prog='tw_timeliness',
                                     description="""Assisiting logic for bulk
                                                    revising timeliness
                                                    related aspects of held
                                                    tasks.""")
    parser.add_argument('--debug',
                        help="""show logic trace""",
                        action='store_true')

    local_dir = os.path.dirname(__file__)
    dflts_file = os.path.join(local_dir, "./cnfg.yml")
    parser.add_argument('-c', '--cnfg',
                        help="""config file to load""",
                        default=dflts_file)

    return parser.parse_args()

ARGS = form_args()
CNFG = Cnfg(ARGS.cnfg).provide()


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

if __name__ == '__main__':
    with daemon.DaemonContext() as context:
        TL.start(block=True)
