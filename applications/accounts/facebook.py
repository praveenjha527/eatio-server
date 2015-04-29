from social.apps.django_app.utils import strategy

import requests

from rest_framework.authentication import get_authorization_header

@strategy()
def register_by_access_token(request, backend):
    backend = request.strategy.backend
    # Split by spaces and get the array
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != 'token':
        msg = 'No token header provided.'
        return msg

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        return msg

    access_token = auth[1]
    # access_token = "CAAEQZBHvok6UBABsReFnp2LdRG0JgJVGo9cctY2aZCEDdMzrPIZCHnyostb4VTE9rGtXFBh1fjPtxZCfvrVEZBWrg1ka8GRNOHmZBAkpXFmPvcSLWZBokjZBu1MC8kyHaeY8wRJqOZA42zfWc2YmUBYyVRu1g5IpwfjJZCa2kZAvcShJFJqMRqsSZAPsc2yeVM8WCZCiG4BevNv6tb8fZBSZBpu9dY1"
    user = backend.do_auth(access_token)

    return user


def disconnect(facebook, *args, **kwargs):
    revoke_url = 'https://graph.facebook.com/{uid}/permissions'.format(uid=facebook.uid)
    params = {'access_token': facebook.extra_data['access_token']}
    response = requests.delete(revoke_url,  params=params)
    
    return response