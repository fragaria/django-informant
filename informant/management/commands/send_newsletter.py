from django.conf import settings
from django.core.management.base import NoArgsCommand

from informant.models import Newsletter


NEWSLETTER_EMAIL = settings.NEWSLETTER_EMAIL


class Command(NoArgsCommand):
    help = "Send undelivered recipes newsletters"

    def handle_noargs(self, **options):
        Newsletter.objects.send_all()
