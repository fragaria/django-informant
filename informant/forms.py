from django import forms


class SubscribleNewsForm(forms.Form):
    email = forms.EmailField()
    surname = forms.CharField(required=False)
    back_url = forms.CharField(required=False)
