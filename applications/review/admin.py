from django.contrib import admin

from applications.review import models
from .time_utils import timesince

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('get_agree_count','get_disagree_count', 'get_time_since', )
    list_display = ('user', 'restaurant', 'review', 'admin_thumbnail', 'get_agree_count','get_disagree_count', 'get_time_since', )
    list_filter = ('good', 'restaurant', )
    search_fields = ('review', )

    def get_agree_count(self, obj):
        return obj.agree_disagrees.filter(agree=True).count()
    get_agree_count.short_description = "Agree Count"

    def get_disagree_count(self, obj):
        return obj.agree_disagrees.filter(agree=False).count()
    get_disagree_count.short_description = "Dis Agree Count"

    def get_time_since(self, obj):
        return timesince(obj.created)

    get_time_since.short_description = "Timesince"

admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.AgreeDisagree)
