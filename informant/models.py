from datetime import datetime
import hashlib

from django.contrib.sites.models import Site
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class Newsletter(models.Model):
    subject = models.CharField(_('Subject'), max_length=128)
    content = models.TextField(_('Content'))
    date = models.DateTimeField(_('Date'), default=datetime.now)
    sent = models.BooleanField(_('Sent'), default=False, editable=False)
    approved = models.BooleanField(_('Approved'), default=False)

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
