from django.contrib import admin

from applications.review import models


admin.site.register(models.Review)
admin.site.register(models.AgreeDisagree)
