from django.contrib import admin

from applications.restaurant import models
from applications.review.models import Review, AgreeDisagree


class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = ('get_agree_count','get_disagree_count',  )
    list_display = ('name', 'city', 'country', 'weight', 'admin_thumbnail','get_disagree_count', 'get_disagree_count', )
    list_filter = ('name', 'country', )
    search_fields = ('name', )

    def get_agree_count(self, obj):
        reviews = Review.objects.filter(restaurant=obj)
        agree_count = 0
        for review in reviews:
            # review total agree_count and disagree_count
            agree_count = AgreeDisagree.objects.filter(review=review, agree=True).count()
        return agree_count
    get_agree_count.short_description = "Agree Count"

    def get_disagree_count(self, obj):
        reviews = Review.objects.filter(restaurant=obj)
        disagree_count =0
        for review in reviews:
            # review total agree_count and disagree_count
            disagree_count = AgreeDisagree.objects.filter(review=review, agree=False).count()
        return disagree_count

    get_disagree_count.short_description = "Dis Agree Count"


admin.site.register(models.Restaurant,RestaurantAdmin)
