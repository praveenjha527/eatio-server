from django import forms
from models import Contact


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput,required=True)

    def __init__(self, * args, ** kwargs):
        super(PasswordForm, self).__init__(*args, ** kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter new password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Enter password again'


    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2