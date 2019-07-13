
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


@TL.job(interval=timedelta(seconds=INTERVAL))
def run(cnfg):
    notifier = Notifier(cnfg)
    for task in Collector(cnfg):
        logger.debug("discerned Tasks>>")
        if discerner.is_exceeding(task):
            logger.debug("--> {0}".format(str(task)))
            notifier.gather(task)

    notifier.release()

if __name__ == '__main__':
    args = form_args()
    cnfg = Cnfg(args.cnfg).provide()
    INTERVAL = cnfg['interval']
    run(cnfg)
    with daemon.DaemonContext() as context:
        TL.start(block=True)
