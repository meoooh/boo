import datetime
from unittest import skip

from rest_framework.test import APITestCase

from wl import models

# Create your tests here.


class Vom(APITestCase):

    def setUp(self):
        user = models.OwlUser.objects.create_user(
            'tset', 'userId', '3', '1990-06-06', 'password')

    def test_create_user_success(self):
        data = {'userId': 'sdf', 'sex': 1, 'deviceId': 'ha', 'password': '1313',
                'password2': '1313', 'birthday': '1990-06-06',
                'gcmId': 'sdfsdf'}
        response = self.client.post('/users', data)

        self.assertEqual(response.status_code, 201)

    def test_check_deviceId(self):
        # import ipdb; ipdb.set_trace()
        data = {u'q': u'test'}
        response = self.client.get('/users/is-exist', data)

        self.assertEqual(response.status_code, 204)
