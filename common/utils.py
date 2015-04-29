import re
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


def is_email(value):
    """
    validating username for username
    :param value:
    :return: boolean
    :rtype :boolean
    """
    email_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE
    )
    return True if email_regex.match(value) else False


def is_mobile(value):
    """
    Check mobile number for value
    :param value:
    :return: boolean
    """
    mobile_regex = re.compile(r'^[1-9]{1}[0-9]{7,10}$')
    return True if mobile_regex.match(value) else False


def remove_extra_whitespace(value):
    """
    Remove extra space fro value
    :param value:
    :return:
    """
    return re.sub(r'\s+', ' ', value).strip()


def name_to_f_name_l_name(name):
    """
    Convert single name to first name and last name
    :param name:
    :return:first_name, last_name
    """
    names = name.split(" ", 1)
    if len(names) == 2:
        return names[0], names[1]
    elif len(names) == 1:
        return names[0], None
    return None, None


def check_0_seqs(value):
    """
    Check value sequence of 0's
    :param value:
    :return:boolean
    """
    matchObj = re.compile(r"(?:0[0])")
    return True if matchObj.match(value) else False


def validate_mobile(value):
    """

    :param value:
    :return:
    """
    if len(str(value)) > 15 or len(str(value)) < 7:
        raise serializers.ValidationError(_("Enter mobile number b/w 7 to 10 digits."))
    elif check_0_seqs(value):
         raise serializers.ValidationError(_("Enter a valid mobile number."))
    return value