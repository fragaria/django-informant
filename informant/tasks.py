from celery.task import Task

from informant.models import Newsletter


__author__ = 'xaralis'


class SendNewslettersTask(Task):
    def run(self, **kwargs):
        return Newsletter.objects.send_all()
