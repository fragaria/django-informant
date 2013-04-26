from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from informant.models import Newsletter, Recipient


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'testing_emails', 'sent', 'approved', 'preview_url',)
    ordering = ('-date',)
    actions = ['reset_sent_flag', 'send_test']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            kwargs['initial'] = render_to_string('informant/mail/newsletter.html')
        return super(NewsletterAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def reset_sent_flag(self, request, queryset):
        queryset.update(sent=False)
    reset_sent_flag.short_description = _('Send again')

    def send_test(self, request, queryset):
        for n in queryset:
            n.send_test()
    send_test.short_description = _('Send to testing emails')


class RecipientAdmin(admin.ModelAdmin):
    fields = ('email', 'sent', 'deleted',)
    list_display = ('email', 'sent', 'deleted', 'date', 'md5',)
    search_fields = ('email',)

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Recipient, RecipientAdmin)
