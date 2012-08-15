Informant
---------

Informant is simple yet flexible app for common newsletter-sending functionality
which lot of sites need to offer. It only provides one common newsletter
with opt-in/opt-out and features management command for mail sending (HTML/text alternative).

Installation
============

Standard Django way::
    
    pip install django-informant
    
Add to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ..
        ..,
        'informant',
        ...
    )
    
Set e-mail address to set newsletters from in your ``settings.py``::

    NEWSLETTER_EMAIL = 'your@example.com
    
Usage
=====
    
Templates
*********

Informant provides few default templates to start with but it's usually better
to make your own - customized. These are:

* ``informant/management/subscribe_ok.html`` - template to render when subscription is OK
* ``informant/management/subscribe_error.html`` - template to render when there was an error
* ``informant/management/unsubscribed.html`` - template to render when user has unsubscribed
* ``informant/mail/newsletter.html`` - base template with e-mail structure
* ``informant/mail/base.txt`` - text alternative that should point out to the web version of the newsletter

Informant uses newsletter text as Django template. It's therefore usefull
to create basic blocks in ``informant/mail/newsletter.html`` and then extend
from it in the newsletter administration and override only specific block
like you would do in real templates. E.g.:

**In informant/mail/newsletter.html**::

    {% load i18n %}
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{% trans "lang" %}" lang="{% trans "lang" %}">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title>{% block head %}{% endblock %}</title>
    </head>
    <body>
    {% block content %}{% endblock %}
    </body>
    </html>


**In Newsletter object content field**::    

    {% extends "informant/mail/newsletter.html" %}
    {% block title %}My title{% endblock %}
    {% block content %}My content{% endblock %}
        

Ajax subscription
*****************

If you don't want separate page with subscription form, Informant has a 
jQuery plugin which will take care.

It is called on the ``<form>`` elements. It expects that form has correctly
set up the action attribute pointing to the right URL. See example::

    <form id="newsletterSubscribeForm" action="{% url "informant_subscribe" %}" method="post">
        <div>
            <label for="email">Enter your e-mail:</label>
            <div id="newsletterSubscribeResult"></div>
            {% csrf_token %}
            <input type="email" name="email" />
            <input type="hidden" name="surname" value="" />
        </div>
        <div>
            <input type="submit" value="Subscribe" class="button" />
        </div>
    </form>

    <script type="text/javascript">
        // JavaScript handler
        var subscribeForm = $('#newsletterSubscribeForm'); 
        subscribeForm.informantSubscribeForm({
            renderResults: true,
            resultContainer: $('#newsletterSubscribeResult')
        });
        subscribeForm.bind('informantSubscribeOk', function () {
           $(this).find('input').hide(); 
        });
    </script>

The Javascript plugin by default doesn't render any results. If you want 
it to, supply configuration as seen above. Plugin will fire ``informantSubscribeOk``
and ``informantSubscribeError`` events in case of successfull or invalid 
subscription respectively. You can bind to these using jQuery's ``.bind()``
method.

Sending
*******

Informant provides ``send_newsletter`` command that will send newsletters
using the email backend from your Django settings.