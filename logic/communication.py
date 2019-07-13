
from smtplib import SMTP
import logging
import jinja2
import os


logger = logging.getLogger(__name__)


class Mailer:

    def __init__(self, cnfg):
        self.cnfg = cnfg
        self._stage_msg_tmplt(cnfg)

    def _stage_msg_tmplt(self, cnfg):
        template_path = cnfg['notifier']['template']
        template_dir = os.path.dirname(template_path)
        template_file = os.path.basename(template_path)

        templateLoader = jinja2.FileSystemLoader(searchpath=template_dir)
        templateEnv = jinja2.Environment(loader=templateLoader)

        self.template = templateEnv.get_template(template_file)

    def dispatch(self, tasks):
        logger.debug("Dispatching with CNFG:")
        logger.debug("{0}".format(self.cnfg))
        msg = self.template.render(tasks=tasks)
        logger.debug("MSG \n {0}".format(msg))
        with SMTP(host=self.cnfg['notifier']['mail_server']['host'],
                  port=self.cnfg['notifier']['mail_server']['port']) as smtp:
            smtp.sendmail(self.cnfg['notifier']['from_addr'],
                          self.cnfg['notifier']['to_addrs'],
                          msg)


class Notifier:
    tasks = list()

    def __init__(self, cnfg):
        if cnfg['notifier']['core'] == 'mailer':
            self.core = Mailer(cnfg)

    def gather(self, task):
        self.tasks.append(task)

    def release(self):
        self.core.dispatch(self.tasks)
