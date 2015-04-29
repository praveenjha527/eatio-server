from __future__ import division
import datetime

from .timezones import utc
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.contrib.auth import get_user_model

def build_url(*args, **kwargs):
    '''
    appends the parameters to the url query string

    :param args: Either pass the url name as an argument,
    :param kwargs: or pass url = 'the absolute url' as a keyword argument
    and pass the parameters as keyword arguments
    :return: url?param1=data1&param2=data2...
    '''
    params = kwargs.pop('params', {})
    url=kwargs.pop('url', {})
    if not url: url = reverse(*args, **kwargs)
    if not params: return url

    qdict = QueryDict('', mutable=True)
    for k, v in params.iteritems():
        if type(v) is list: qdict.setlist(k, v)
        else: qdict[k] = v

    return url + '?' + qdict.urlencode()

def iso_format_to_datetime(iso_format):
    relevant_str = iso_format.split('+')[0]
    date, time = relevant_str.split('T')
    year, month, day = map(int, date.split('-'))
    hour, minute, second = map(float, time.split(':'))
    hour, minute, second = map(int, (hour, minute, second))
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=utc)


def datetime_to_iso_format(dt):
    utc_datetime = dt.replace(tzinfo=utc)
    return utc_datetime.isoformat()



def clean_to_email_field(email):
    """
    Returns a filtered email address for gmail.com and googlemail.com addresses with no dots
    :param email:
    :return:
    """
    import re
    x = re.search(r'([\w.-]+)@([\w.-]+)', email)
    domain = x.group(2)
    email_id = x.group(1)

    if domain in ['gmail.com', 'googlemail.com']:
        email_id = email_id.replace(".","")
        return email_id+'@'+domain
    else:
        return email


def get_admin():
    return get_user_model().objects.get(username="eatio")

def create_referral_code(email):
    return "eatio" + email.split("@")[0]
