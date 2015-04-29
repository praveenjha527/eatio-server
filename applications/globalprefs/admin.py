from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import AppPreferences


admin.site.register(AppPreferences, SingletonModelAdmin)