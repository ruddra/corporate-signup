"""
User Form
"""
from django import forms

from users.services import UserService


class UserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    retype_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', None)
        password, re_password = cleaned_data.get(
            'password', None), cleaned_data.get('retype_password', None)
        try:
            UserService().validate_email(email)
            UserService().validate_password(password, re_password)
        except Exception as ex:
            raise forms.ValidationError(str(ex))
        return cleaned_data
