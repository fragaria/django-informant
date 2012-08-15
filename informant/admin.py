from django.contrib import admin
from django.template.loaders.app_directories import Loader

from informant.models import Newsletter, Recipient


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'sent', 'approved', 'preview_url',)
    ordering = ('-date',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            l = Loader()
            kwargs['initial'] = l.load_template_source('informant/mail/newsletter.html')[0]
        return super(NewsletterAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class RecipientAdmin(admin.ModelAdmin):
    fields = ('email', 'sent', 'deleted',)
    list_display = ('email', 'sent', 'deleted', 'date', 'md5',)
    search_fields = ('email',)

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Recipient, RecipientAdmin)
