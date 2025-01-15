from django import forms
from .models import Partner


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ('bookstore', 'phone_number', 'email', 'county',)
 