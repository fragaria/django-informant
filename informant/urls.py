from django.conf.urls.defaults import patterns, url
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('informant.views',
    url('^%s/$' % slugify(_('subscribe')),
        'subscribe',
        name='informant_subscribe'),
    url('^%s/([0-9a-f]{32})/$' % slugify(_('unsubscribe')),
        'unsubscribe',
        name='informant_unsubscribe'),
    url('^%s/([0-9]*)/$' % slugify(_('preview')),
        'preview',
        name='informant_preview'),
)
