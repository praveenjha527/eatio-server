from redis import ConnectionError

__author__ = 'somghosh'

from mixpanel.tasks import EventTracker, PeopleTracker
from apps.accounts.models import User
from voltbe2 import settings


def add_or_update_user_to_mixpanel(user):
    PeopleTracker.delay('set',
                        {
                            'distinct_id': user.id,
                            '$first_name': user.first_name,
                            '$last_name': user.last_name,
                            '$email': user.email,
                            'Date Joined': user.date_joined.isoformat(),
                            '$ignore_time': True,
                            'Gender': user.gender,
                            'Location City': user.location_city

                        })


def update_all_users_to_mixpanel():
    for u in User.objects.filter(is_staff=False).filter(is_superuser=False):
        add_or_update_user_to_mixpanel(u)
        add_signup_event_to_mixpanel(u)


def import_past_point_into_mixpanel(dict_to_import):
    import requests
    import json
    import base64

    string_data = json.dumps(dict_to_import)
    encoded_data = base64.b64encode(string_data)
    payload = {
        'data': encoded_data,
        'api_key': settings.MIXPANEL_API_KEY}
    return requests.post('http://api.mixpanel.com/import/', params=payload)


def add_activity_to_mixpanel(activity):
    from dateutil.relativedelta import relativedelta
    from datetime import datetime, date

    user = activity.main_user
    age = relativedelta(datetime.today(), user.age, ).years
    days_on_em = (datetime.today() - user.date_joined.replace(tzinfo=None)).days

    activity_dict = {'event': settings.DID_ACTIVITY,
                     'properties':
                         {
                             'distinct_id': user.id,
                             'Username': user.__str__(),
                             'Age': age,
                             'Gender': user.gender,
                             'Days on Earthmiles': days_on_em,
                             'Total Earthmiles': user.total_earthmiles,
                             'Redeemable Earthmiles': user.redeemable_earthmiles,
                             'time': activity.time_started.isoformat(),
                             'Activity ID': activity.id,
                             'Points': activity.points,
                             'Activity Source': activity.activity_source,
                             'Duration mins': getattr(activity, 'total_duration', 0),
                             'Distance kms': getattr(activity, 'total_distance', 0),
                             'Activity Type': getattr(activity, 'activity_type', 'Not tracked activity'),
                             'Eligible': activity.is_eligible_for_points,
                             'token': settings.MIXPANEL_API_TOKEN
                         }
    }
    return import_past_point_into_mixpanel(activity_dict)


def import_past_activities():
    from apps.activity.running.models import TrackedFitnessActivity

    for b in TrackedFitnessActivity.objects.all():
        add_activity_to_mixpanel(b)


def add_signup_event_to_mixpanel(user):
    activity_dict = {'event': '$signup',
                     'properties':
                         {
                             'distinct_id': user.id,
                             'time': user.date_joined.isoformat(),
                             'token': settings.MIXPANEL_API_TOKEN,
                         }
    }
    return import_past_point_into_mixpanel(activity_dict)


def send_mixpanel_event(event_name, user, event_dict=None):
    """
    Helper function that takes from various views an event name, an event_dict and an user and populates the event dict with
    a) distinct_id of the user with key 'distinct_id'
    b) 'username' = user.firstname + user.lastname
    c) 'age' = in years, today - DOB
    d) 'gender' = user.gender
    e) total em
    f) redeemable em
    g) time on earthmiles = today - joining date
    and then calls EventTracker.delay() with the modified dictionary
    """
    from dateutil.relativedelta import relativedelta
    from datetime import datetime, date

    if event_dict == None:
        event_dict = {}
    try:
        age = relativedelta(datetime.today(), user.age, ).years
        days_on_em = (datetime.today() - user.date_joined.replace(tzinfo=None)).days
        event_dict.update(
            {
                'distinct_id': user.id,
                'Username': user.__str__(),
                'Age': age,
                'Gender': user.gender,
                'Days on Earthmiles': days_on_em,
                'Total Earthmiles': user.total_earthmiles,
                'Redeemable Earthmiles': user.redeemable_earthmiles,
            }
        )
    except AttributeError as e:
        event_dict.update(
            {
                'distinct_id': user.id,
            }
        )


    #Try to send event to mixpanel. If there is an error, it could be because we're testing on localhost, in which case, pass, else raise the error
    try:
        EventTracker.delay(event_name, event_dict)
    except ConnectionError as e:
        if 'localhost' not in str(e):
            raise
