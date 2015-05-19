from applications.restaurant.models import Restaurant
from applications.review.models import Review, AgreeDisagree


def execute_calculation():
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

