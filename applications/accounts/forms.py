from django import forms
from django.contrib.auth.forms import UserCreationForm

from applications.accounts.models import User


class UserCreationAdminForm(UserCreationForm):
    """
    Override to use custom user model in django admin user creation
    """
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )