
from logic import core
from logic import discerner

import unittest
import collections
import os
import glob
import datetime as dt
import threading
from taskw import TaskWarrior

import logging
import os
import yaml


class timeTesting(unittest.TestCase):

    def stage_tw(self):
        overrides = {'data': {'location':  os.path.join(self.local_dir,
                                                        'task')}}
        rc_file = os.path.join(self.local_dir,
                               "./cnfg/taskrc")
        tw = TaskWarrior(config_filename=rc_file,
                         config_overrides=overrides)
        self.tw = tw

    def setUp(self):

        def alter_cnfg(_file):
            smtp_credential = os.environ['SMTP_CREDENTIAL']
            cnfg = core.Cnfg(file=_file).provide()
            (cnfg['notifier']
                 ['mail_server']
                 ['password']) = smtp_credential

            with open(_file, "w") as fp:
                fp.write(yaml.dump(cnfg))

        self.local_dir = os.path.dirname(__file__)

        self.stage_tw()

        self.form_test_items()

        cnfg_file = os.path.join(self.local_dir,
                                 "./cnfg.yml")

        alter_cnfg(cnfg_file)

        args = collections.namedtuple('args', ['cnfg'])
        args.cnfg = cnfg_file
        core.start(args, oneshot=True)

    def tearDown(self):
        data_reside = os.path.join(self.local_dir, "task", "*.data")
        for tw_data_f in glob.glob(data_reside):
            os.remove(tw_data_f)

    def form_test_items(self):
        self.tw.task_add("TaskA", project="ProjA",
                         scheduled="20190630T120000Z",
                         due="20190701T120000Z1")
        self.tw.task_add("TaskB", project="ProjA",
                         scheduled="20190701T120000Z",
                         due="20190702T120000Z1")
        self.tw.task_add("TaskC", project="ProjB",
                         scheduled="20190710T120000Z",
                         due="20190715T120000Z1")

    def test_none(self):
        discerner.NOW = dt.datetime.strptime("20190620T120000Z",
                                             discerner.TASK_DATE_FMT)
        core.run()

        # assert local mails
