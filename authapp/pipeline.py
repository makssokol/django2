from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ArtShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(
        ('https',
         'api.vk.com',
         '/method/users.get',
         None,
         urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                               access_token=response['access_token'],
                               v='5.92')),
         None
         ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data.get('sex'):
        user.artshopuserprofile.gender = \
            ArtShopUserProfile.MALE if data['sex'] == 2 else ArtShopUserProfile.FEMALE

    if data.get('about'):
        user.artshopuserprofile.aboutMe = data['about']

    if data.get('bdate'):
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
