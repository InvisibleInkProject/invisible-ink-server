from tastypie.test import ResourceTestCase
from resources import Message, User

from django.test import client

from provider.oauth2 import models

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class AuthenticationTestCase(ResourceTestCase):

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    #TODO: This is too big of a setup method. And should probably be 
    #      refactored into a bit nicer thing
    #      Pershaps something with fixtures
    def setUp(self):
        super(AuthenticationTestCase, self).setUp()

        self.username = 'mark1'
        self.password = 'polak2'
        self.user = User.objects.create_user(
                            self.username, 
                            'mark@thedutchies.com', 
                            self.password, 
                            age=20
                    )
        self.user = User.objects.create_user(
                            'user2', 
                            'mark@thedutchies.com', 
                            'user2pass', 
                            age=19
                    )

        Message.objects.create(
                user = self.user,
                text = "Test message",
                location_lat = 10.0,
                location_lon = 10.0,
                radius = 10
        )

        self.client = models.Client(
                user=self.user, 
                name="mysite client", 
                client_type=1, 
                url="http://thedutchies.com"
        )
        self.client.save()

        self.access_token_data = {
                'client_id': self.client.client_id,
                'client_secret': self.client.client_secret,
                'grant_type': 'password',
                'username': self.username,
                'password': self.password,
                'scope': 'write'
        }

        #Generate a access_token
        resp = client.Client().post(
                '/oauth2/access_token', 
                format='application/x-www-form-urlencoded', 
                data=self.access_token_data
        )
        self.access_token = models.AccessToken.objects.get(id=1)

        self.db_entry = Message.objects.get(id=1)

        self.message_data = {
                'text': 'This is a test',
                'location_lon': 10.0,
                'location_lat': 10.0,
                'radius': 10.0
        }

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def get_credentials(self):
        return 'OAuth %s' % self.access_token

    def get_first_message_from_api(self):
        return self.api_client.get(
                '/api/v1/message/1/', 
                format='json', 
                authentication=self.get_credentials()
        )

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_access_denied_for_normal_request(self):
        self.assertHttpUnauthorized(
                self.api_client.get(
                        '/api/v1/message/10.0,10.0,10.0/', 
                        format='json'
                )
        )        

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_get_all_messages(self):
        resp = self.api_client.get(
                '/api/v1/message/10.0,10.0,10.0/', 
                format='json', 
                authentication=self.get_credentials()
        )
        self.assertValidJSONResponse(resp)

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_access_denied_for_single_message(self):
        self.assertHttpUnauthorized(
                self.api_client.get('/api/v1/message/1/', format='json')
        )
    
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_get_message_response_keys(self):
        message_keys = [
                u'id', u'created', u'updated', u'expires', u'text', 
                u'location_lat', u'location_lon', u'radius', 
                u'distance', u'resource_uri'
        ]

        resp = self.get_first_message_from_api()

        self.assertValidJSONResponse(resp)
        self.assertKeys(self.deserialize(resp), message_keys)

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_get_a_single_message(self):
        resp = self.get_first_message_from_api()

        #Check if it is indeed the same message
        self.assertEqual(self.deserialize(resp)['id'], self.db_entry.id)
        self.assertEqual(self.deserialize(resp)['text'], self.db_entry.text)

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_access_denied_for_posting_a_message(self):
        self.assertHttpUnauthorized(
            resp = self.api_client.post(
                    '/api/v1/message/',
                    format='json',
                    data=self.message_data,
            )
        )

    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def test_posting_a_message(self):
        initial_message_count = Message.objects.count()

        resp = self.api_client.post(
                '/api/v1/message/',
                format='json',
                data=self.message_data,
                authentication=self.get_credentials()
        )

        self.assertHttpCreated(resp)
        self.assertEquals(Message.objects.count(), initial_message_count + 1)
