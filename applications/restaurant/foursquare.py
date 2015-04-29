import requests
try:
    # for python3.4
    from urllib.parse import urljoin
except ImportError:
    # for python2.7 support
    from urlparse import urljoin


from django.conf import settings
from django.utils import timezone


def get_restaurant_details_from_foursquare(external_id):
    """
    Example::
        {
        external_id:134456,
        name:"name",
        image:"image url",
        address:"address",
        city:"city",
        }
    Create a restaurant.Restaurant from foursquare
    :param restaurant_id:
    :return:
    """
    return FourSquare().get_venue(external_id)


class FourSquareException(Exception):
    pass


class FourSquare(object):
    """
    Class that interact with foursquare
    """
    def __init__(self):
        self.client_id = settings.FOURSQUARE_CLIENT_ID
        self.client_secret = settings.FOURSQUARE_CLIENT_SECRET
        self.category_id = settings.FOURSQUARE_CATEGORY_ID
        self.intent = settings.FOURSQUARE_INTENT
        self.radius = settings.FOURSQUARE_RADIUS


    def get_venue(self, external_id):
        venue_detail_url = settings.FOURSQUARE_VENUE_DETAIL_API_URL
        venue_detail_url = urljoin(venue_detail_url, external_id)
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "v": self.get_formatted_date(),
        }
        response_json = requests.get(venue_detail_url, params=params).json()
        try:
            return self._format_json_venue(response_json['response']['venue'], detail=True)
        except (FourSquareException, KeyError):
            raise FourSquareException(
                response_json['meta']['errorDetail'] if response_json.get(
                    "meta") and response_json['meta'].get('errorDetail') else "server error")

    def search_venues(self, lat, lng):
        venue_search_url = settings.FOURSQUARE_VENUE_SEARCH_API_URL
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "categoryId": self.category_id,
            "intent": self.intent,
            "radius": self.radius,
            "ll": "%s,%s" % (lat,lng),
            "v": self.get_formatted_date(),
        }
        response_json = requests.get(venue_search_url, params=params).json()
        try:
            venues = response_json['response']['venues']
            return self._format_venues(venues)
        except (FourSquareException, KeyError):
            raise FourSquareException(
                response_json['meta']['errorDetail'] if response_json.get(
                    "meta") and response_json['meta'].get('errorDetail') else "server error")

    def _format_venues(self, venues):
        return [self._format_json_venue(venue) for venue in venues]

    def _format_json_venue(self, venue, detail=False):
        formated_venue = {
        "external_id":venue.get('id'),
        "name":venue.get('name'),
        "distance":venue['location']['distance'] if venue.get(
            'location') and venue['location'].get('distance') else None,
        "address":venue['location']["formattedAddress"][0] if venue.get(
            'location') and venue['location'].get('formattedAddress') else None,
        "city":venue['location']['city'] if venue.get('location') and venue['location'].get('city') else None,
        "country":venue['location']['country'] if venue.get('location') and venue['location'].get('country') else None,
        }
        if detail:
            formated_venue['image'] = self._get_image_from_json(venue)
            formated_venue['lat'] = venue['location']['lat'] if venue.get(
                'location') and venue['location'].get('lat') else ""
            formated_venue['lng'] = venue['location']['lng'] if venue.get(
                'location') and venue['location'].get('lng') else ""
        return formated_venue

    def _get_image_from_json(self, venue):
        """
        Create image url from suffix and prefix with image size
        :param venue:
        :return:
        """
        if venue.get('bestPhoto'):
            prefix = venue['bestPhoto']['prefix']
            suffix = "%s%s" % (settings.FOURSQUARE_PHOTO_SIZE, venue['bestPhoto']['suffix'])
            return urljoin(prefix, suffix)

    @staticmethod
    def get_formatted_date():
        now = timezone.now()
        return "%d%02d%02d" % (now.year, now.month, now.day)

# https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id=SWODPYUXPE4PVBZDF3R1DXLQFIT4QSSEBBZMYTPCDBHXRFQD&client_secret=QY4LPUTYFB5OGOYJA4352SOK54NA35QUJHO3XLU2GKKBG0UQ&v=20150418&categoryId=4d4b7105d754a06374d81259
# https://api.foursquare.com/v2/venues/4c36476d93db0f47f6cc1d92?client_id=SWODPYUXPE4PVBZDF3R1DXLQFIT4QSSEBBZMYTPCDBHXRFQD&client_secret=QY4LPUTYFB5OGOYJA4352SOK54NA35QUJHO3XLU2GKKBG0UQ&v=20150418