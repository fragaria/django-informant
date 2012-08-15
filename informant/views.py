from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404, HttpResponseRedirect, \
    HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template import Template, Context


from informant.models import Recipient, Newsletter
from informant.forms import SubscribleNewsForm


def subscribe(request):
    if request.method == 'POST':
        f = SubscribleNewsForm(request.POST)

        if f.is_valid():
            # Drop spam - field surname must be empty
            if f.cleaned_data['surname'] != '':
                return HttpResponseForbidden()

            # Save email
            if Recipient.objects.filter(email=f.cleaned_data['email']).count() == 0:
                # If email doesn't exist, save email
                r = Recipient(email=f.cleaned_data['email'])
                r.save()
            else:
                # If email exists, clear deleted flag and set new created date
                r = Recipient.objects.get(email=f.cleaned_data['email'])
                r.sent = False
                r.deleted = False
                r.date = None
                r.save()

            if not request.is_ajax():
                url = f.cleaned_data['back_url']
                return HttpResponseRedirect(url)
            else:
                return render(
                    request,
                    'informant/management/subscribe_ok.html',
                    {'subscribe_email': r.email})
        else:
            url = request.POST.get('back_url', '/')
            email = request.POST.get('email', '@')
            return render(
                request,
                'informant/management/subscribe_error.html',
                {'back_url': url, 'subscribe_email': email},
                status=400)
    raise Http404


def unsubscribe(request, recipient_hash):
    try:
        r = Recipient.objects.get(md5=recipient_hash, deleted=False)
    except:
        # Recipient does not exist
        return HttpResponseForbidden()

    r.deleted = True
    r.save()

    return render(request,
                  'informant/management/unsubscribed.html',
                  {'recipient': r})


def preview(request, pk):
    # If newsletter doesn't exist, return 404
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # If newsletter has not been sent and user has not been logged, return 404
    if not newsletter.approved and not request.user.is_authenticated():
        raise Http404

    md5_mark = '00112233445566778899aabbccddeeff'

    c = Context({
        'newsletter': newsletter,
        'site': Site.objects.get_current(),
        'recipient': {'md5': md5_mark},
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL
    })
    t = Template(newsletter.content)

    return HttpResponse(t.render(c))
