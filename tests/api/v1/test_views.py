from unittest import mock
import json

from tests.api.utils import APITestCase
from url_shortener.models import db
from url_shortener.models import MobileRedirect, TabletRedirect, DesktopRedirect, \
    MOBILE_TYPE_STRING, DESKTOP_TYPE_STRING, TABLET_TYPE_STRING


class TestViews(APITestCase):

    def setUp(self):
        super().setUp()
        self.long_url = 'http://www.google.com'
        self.tablet_long_url = 'http://www.linkedin.com'
        self.mobile_long_url = 'http://news.ycombinator.com'
        self.hashed_id = 'v'
        with self.app.app_context():
            db.session.add_all([
                DesktopRedirect(
                    id=21,
                    hashed_id=self.hashed_id,
                    long_url=self.long_url
                ),
                TabletRedirect(
                    id=22,
                    hashed_id=self.hashed_id,
                    long_url=self.tablet_long_url
                ),
                MobileRedirect(
                    id=23,
                    hashed_id=self.hashed_id,
                    long_url=self.mobile_long_url
                )
            ])
            db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_hashed_id_not_found(self):
        response = self.send_get_request_from_desktop_of('e')

        self.assertEqual(404, response.status_code)

    def test_redirect_from_different_devices(self):
        response = self.send_get_request_from_desktop_of('v')

        self.assertEqual(302, response.status_code)
        self.assertEqual(self.long_url, response.location)

        response = self.send_get_request_from_tablet_of('v')

        self.assertEqual(302, response.status_code)
        self.assertEqual(self.tablet_long_url, response.location)

        response = self.send_get_request_from_mobile_of('v')

        self.assertEqual(302, response.status_code)
        self.assertEqual(self.mobile_long_url, response.location)

    def test_submit_long_url(self):
        long_url_dict = {'longUrl': 'http://www.google.com'}
        response = self.client.post(
            '/v1/redirects',
            data=json.dumps(long_url_dict),
            content_type='application/json'
        )

        self.assertEqual(200, response.status_code)

    def test_get_all_existing_redirects(self):
        expected_elapsed_time = 10

        expected_json_payload = {
            'v': [
                {
                    'type': 'desktop',
                    'longUrl': self.long_url,
                    'sinceCreation': expected_elapsed_time,
                    'redirectCount': 0
                },
                {
                    'type': 'tablet',
                    'longUrl': self.tablet_long_url,
                    'sinceCreation': expected_elapsed_time,
                    'redirectCount': 0
                },
                {
                    'type': 'mobile',
                    'longUrl': self.mobile_long_url,
                    'sinceCreation': expected_elapsed_time,
                    'redirectCount': 0
                }
            ]
        }

        with mock.patch(
                'url_shortener.api.v1.views.elapsed_time_in_seconds_since'
        ) as elapsed_time_mock:
            elapsed_time_mock.return_value = expected_elapsed_time
            response = self.client.get(
                '/v1/redirects'
            )

        data = json.loads(response.data)
        self.assertDictEqual(data, expected_json_payload)

    def test_update_long_urls_for_hashed_id_in_two_steps(self):
        updated_desktop_long_url = 'https://twitter.com/'

        desktop_type_to_updated_long_url_dict = {
            DESKTOP_TYPE_STRING: updated_desktop_long_url
        }
        uri = "{}/{}".format('/v1/redirects', self.hashed_id)

        response = self.client.patch(
            uri,
            data=json.dumps(desktop_type_to_updated_long_url_dict),
            content_type='application/json'
        )

        desktop_redirect_instance, tablet_redirect_instance, mobile_redirect_instance = self.retrieve_all_devices_redirects_for(self.hashed_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            updated_desktop_long_url,
            desktop_redirect_instance.long_url
        )
        self.assertEqual(
            self.tablet_long_url,
            tablet_redirect_instance.long_url
        )
        self.assertEqual(
            self.mobile_long_url,
            mobile_redirect_instance.long_url
        )

        updated_tablet_long_url = 'https://www.facebook.com/'
        updated_mobile_long_url = 'https://www.instagram.com/'
        other_types_to_updated_long_url_dicts = {
            MOBILE_TYPE_STRING: updated_mobile_long_url,
            TABLET_TYPE_STRING: updated_tablet_long_url
        }

        response = self.client.patch(
            uri,
            data=json.dumps(other_types_to_updated_long_url_dicts),
            content_type='application/json'
        )

        self.assertEqual(200, response.status_code)
        desktop_redirect_instance, tablet_redirect_instance, mobile_redirect_instance = self.retrieve_all_devices_redirects_for(self.hashed_id)
        self.assertEqual(
            updated_desktop_long_url,
            desktop_redirect_instance.long_url
        )
        self.assertEqual(
            updated_tablet_long_url,
            tablet_redirect_instance.long_url
        )
        self.assertEqual(
            updated_mobile_long_url,
            mobile_redirect_instance.long_url
        )
