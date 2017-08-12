"""
Bill Modelform
"""
from django import forms
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField


class BillForm(forms.Form):
    address = forms.CharField()
    current_city = forms.CharField(required=False)
    country = LazyTypedChoiceField(choices=countries)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
