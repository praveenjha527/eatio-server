from django.core.management.base import BaseCommand, CommandError

from applications.restaurant.models import Restaurant
from applications.review.models import Review, AgreeDisagree


class Command(BaseCommand):
    """
    Command to update restaurant weight.
    """

    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        restaurants = Restaurant.objects.all()

        for restaurant in restaurants:
            reviews = Review.objects.filter(restaurant=restaurant)
            weight = 0
            for review in reviews:
                # review total agree_count and disagree_count
                agree_count = AgreeDisagree.objects.filter(review=review, agree=True).count()
                disagree_count = AgreeDisagree.objects.filter(review=review, agree=False).count()

                if review.good:
                  weight = weight+agree_count-disagree_count+1

                if not review.good:
                  weight = weight-agree_count+disagree_count-1

            # saves restaurant total weight
            restaurant.weight = weight
            restaurant.save()