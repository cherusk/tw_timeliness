
import unittest
import os
import glob
import datetime as dt
from taskw import TaskWarrior
from logic import Collector
from logic import core
from logic import discerner

import smtpd.DebuggingServer as TestMailServer


class timeTesting(unittest.TestCase):

    def load_tw_cnfg(self):
        return os.path.join(self.local_dir, "./cnfg/.taskrc")

    def stage_tw(self, cnfg_file):
        overrides = {'data': {'location':  os.path.join(self.local_dir,
                     'task')}}
        tw = TaskWarrior(config_filename=cnfg_file,
                         config_overrides=overrides)
        self.tw = tw

    def setUp(self):
        self.local_dir = os.path.dirname(__file__)
        cnfg_file = self.load_tw_cnfg()
        self.stage_tw(cnfg_file)

        self.form_test_items()

        self.tasks = Collector(cnfg_file)

        local_dir = os.path.dirname(__file__)
        cnfg_file = os.path.join(local_dir,
                                 "./cnfg.yml")
        core.ARGS.cnfg = cnfg_file
        self.mail_server = TestMailServer(("localhost", 25),
                                          ("localhost", 25))

    def tearDown(self):
        data_reside = os.path.join(self.local_dir, "task", "*.data")
        for tw_data_f in glob.glob(data_reside):
            os.remove(tw_data_f)

    def form_test_items(self):
        self.tw.task_add("TaskA", project="ProjA",
                         scheduled="20190630T120000Z1",
                         due="20190701T120000Z1")
        self.tw.task_add("TaskB", project="ProjA",
                         scheduled="20190701T120000Z1",
                         due="20190702T120000Z1")
        self.tw.task_add("TaskC", project="ProjB",
                         scheduled="20190710T120000Z1",
                         due="20190715T120000Z1")

    def test_none(self):
        discerner.NOW = dt.datetime.strptime("20190620T120000Z1",
                                             discerner.TASK_DATE_FMT)
        core.run()

        # assert local mails
