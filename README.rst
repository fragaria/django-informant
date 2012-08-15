Informant
---------

Informant is simple yet flexible app for common newsletter-sending functionality
which lot of sites need to offer. It only provides one common newsletter
with opt-in/opt-out and features management command for mail sending (HTML/text alternative).

Installation
============

Standard Django way::
    
    pip install informant
    
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
* ``informant/management/subscribe_error.html`` - template to render when there was and error
* ``informant/management/unsubscribed.html`` - template to render when user has unsubscribed
* ``informant/mail/newsletter.html`` - base template with e-mail structure
* ``informant/mail/base.txt`` - text alternative that should point out to the web version of the newsletter

Informant uses newsletter text as Django template. It's therefore usefull
to create basic blocks in ``informant/mail/newsletter.html`` and then
only override them in the administration.

Sending
*******

Informant provides ``send_newsletter`` command that will send newsletters
using the email backend from your Django settings.