
from notifiers import get_notifier
from notifiers.utils import  helpers
import collections
import jinja2
import os
from introspection import load_logger


logger = load_logger()


class Notifier:
    tasks = collections.defaultdict(list)

    def __init__(self, cnfg):
        self.cnfg = cnfg
        self.core = get_notifier(cnfg['notifier']['type'])
        self._stage_msg_tmplt(cnfg)

    def _stage_msg_tmplt(self, cnfg):
        template_path = (cnfg['notifier']
                             ['content']
                             ['msg_template_file'])
        template_dir = os.path.dirname(template_path)
        template_file = os.path.basename(template_path)

        templateLoader = jinja2.FileSystemLoader(searchpath=template_dir)
        templateEnv = jinja2.Environment(loader=templateLoader)

        self.template = templateEnv.get_template(template_file)

    def gather(self, task, categories):
        for category in categories:
            self.tasks[category].append(task)

    def release(self):
        logger.debug("Dispatching with CNFG:")
        logger.debug("{0}".format(self.cnfg))
        msg = self.template.render(tasks=self.tasks)
        logger.debug("MSG \n {0}".format(msg))

        notifier_cnfg = self.cnfg['notifier']
        del notifier_cnfg['content']['msg_template_file']
        params = helpers.merge_dicts(notifier_cnfg['mail_server'],
                                     notifier_cnfg['content'])
        self.core.notify(from_=notifier_cnfg['from_addr'],
                         to=notifier_cnfg['to_addrs'],
                         message=msg,
                         **params)
