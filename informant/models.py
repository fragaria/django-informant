from datetime import datetime
import hashlib
import logging
import re
import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db import models
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


if hasattr(settings, 'INFORMANT_TESTING_EMAILS'):
    TESTING_EMAILS = settings.INFORMANT_TESTING_EMAILS
elif settings.MANAGERS:
    TESTING_EMAILS = [m[1] for m in settings.MANAGERS]
else:
    TESTING_EMAILS = ''

try:
    NEWSLETTER_EMAIL = settings.NEWSLETTER_EMAIL
except AttributeError:
    raise ImproperlyConfigured('NEWSLETTER_EMAIL setting is missing but required.')


# Fake md5
MD5_MARK = '00112233445566778899aabbccddeeff'
MD5_MARK_PATT = re.compile(MD5_MARK)


logger = logging.getLogger(__name__)


class NewsletterManager(models.Manager):
    def send_all(self):
        translation.activate(settings.LANGUAGE_CODE)

        # Newsletters, which have approved and have not delivered
        newsletters = Newsletter.objects.filter(approved=True, sent=False,
                                                date__lte=datetime.now())
        connection = get_connection()

        for newsletter in newsletters:
            newsletter.send(connection=connection)


class Newsletter(models.Model):
    subject = models.CharField(_('Subject'), max_length=128)
    content = models.TextField(_('Content'))
    date = models.DateTimeField(_('Date'), default=datetime.now)
    sent = models.BooleanField(_('Sent'), default=False, editable=False)
    testing_emails = models.CharField(_('Testing emails'), max_length=255, default=TESTING_EMAILS)
    approved = models.BooleanField(_('Approved'), default=False)

    objects = NewsletterManager()

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ('date',)

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        return ('informant_preview', (self.pk,))

    def get_domain_url(self):
        return 'http://%s%s' % (
            Site.objects.get_current().domain,
            self.get_absolute_url()
        )

    def preview_url(self):
        return mark_safe('<a target="_blank" href="%s">URL</a>' % self.get_absolute_url())
    preview_url.allow_tags = True
    preview_url.short_description = _('Preview')

    def _prep_content(self):
        # Prepare context
        c = Context({
            'newsletter': self,
            'site': Site.objects.get_current(),
            'recipient': {'md5': MD5_MARK},
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL
        })

        # Render parts
        content_html_ = Template(self.content).render(c)
        content_txt_ = render_to_string('informant/mail/base.txt', c)

        return content_html_, content_txt_

    def send(self, connection=None):
        content_html_, content_txt_ = self._prep_content()

        # Recipients, who have not got newsletter
        recipients = Recipient.objects.filter(sent=False, deleted=False)

        for recipient in recipients:
            # Replace fake md5
            content_html = re.sub(MD5_MARK_PATT, recipient.md5, content_html_)
            content_txt = re.sub(MD5_MARK_PATT, recipient.md5, content_txt_)

            # Send mail
            msg = EmailMultiAlternatives(self.subject, content_txt,
                                         NEWSLETTER_EMAIL, (recipient.email,))
            msg.attach_alternative(content_html, 'text/html')

            try:
                if connection is None:
                    connection = get_connection()
                connection.send_messages((msg,))
            except Exception, e:
                logger.warning('Couldnt deliver: %s - %s' % (recipient.email, str(e)))

            # Set recipient delivered flag
            recipient.sent = True
            recipient.save()

        # If newsletter was sent, set newsletter delivered flag
        self.sent = True
        self.save()

        # And clear recipients delivered flag
        Recipient.objects.all().update(sent=False)

    def send_test(self):
        content_html, content_txt = self._prep_content()

        recipients = self.testing_emails.split(',')

        # Send mail
        msg = EmailMultiAlternatives(self.subject, content_txt,
                                     NEWSLETTER_EMAIL, recipients)
        msg.attach_alternative(content_html, 'text/html')

        try:
            connection = get_connection()
            connection.send_messages((msg,))
        except Exception, e:
            logger.warning('Couldnt deliver: %s' % str(e))


class Recipient(models.Model):
    email = models.EmailField(_('Email'))
    date = models.DateTimeField(_('Created'))
    sent = models.BooleanField(_('Sent'), default=False)
    deleted = models.BooleanField(_('Deleted'), default=False)
    md5 = models.CharField(_('MD5'), max_length=32)

    class Meta:
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipients')
        ordering = ('email',)

    def __unicode__(self):
        return self.email

    def do_md5(self):
        m = hashlib.md5()
        m.update(self.email)
        m.update(str(self.date))
        return m.hexdigest()

    def save(self, *args, **kwargs):
        if self.date == None or self.md5 == None:
            self.date = datetime.now()
            self.md5 = self.do_md5()

        super(Recipient, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'username': self.email
        }
