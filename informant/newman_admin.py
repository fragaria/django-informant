'''
Created on 10.10.2011

@author: xaralis
'''

from django.template.loaders.app_directories import Loader
import ella_newman as newman

from informant.models import Newsletter, Recipient

class NewsletterAdmin(newman.NewmanModelAdmin):
    list_display = ('subject', 'date', 'sent', 'approved', 'preview_url',)
    ordering = ('-date',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            l = Loader()
            kwargs['initial'] = l.load_template_source('newsletters/mail/body/iw-newsletter.html')[0]
        return super(NewsletterAdmin, self).formfield_for_dbfield(db_field, **kwargs)

class RecipientAdmin(newman.NewmanModelAdmin):
    fields = ('email', 'sent', 'deleted',)
    list_display = ('email', 'sent', 'deleted', 'date', 'md5',)
    search_fields = ('email',)

newman.site.register(Newsletter, NewsletterAdmin)
newman.site.register(Recipient, RecipientAdmin)
