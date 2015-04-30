__author__ = 'sayone'

from django.contrib import admin

from applications.web import models


admin.site.register(models.Contact)
