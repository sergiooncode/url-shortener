from unittest import TestCase

from url_shortener import create_app
from url_shortener.models import db
from url_shortener.models import MobileRedirect, TabletRedirect, DesktopRedirect


class APITestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.app = create_app()
        db.create_all(app=self.app)
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all(app=self.app)

    def send_get_request_from_desktop_of(self, hashed_id):
        response = self.client.get(
            "/{}".format(hashed_id),
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"})
        return response

    def send_get_request_from_mobile_of(self, hashed_id):
        response = self.client.get(
            "/{}".format(hashed_id),
            headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B202 Safari/604.1"})
        return response

    def send_get_request_from_tablet_of(self, hashed_id):
        response = self.client.get(
            "/{}".format(hashed_id),
            headers={"User-Agent": "Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1"})
        return response

    def retrieve_all_devices_redirects_for(self, hashed_id):
        desktop_redirect_instance = None
        tablet_redirect_instance = None
        mobile_redirect_instance = None
        with self.app.app_context():
            desktop_redirect_instance = db.session.query(DesktopRedirect).filter_by(
                hashed_id=self.hashed_id
            ).first()
            tablet_redirect_instance = db.session.query(TabletRedirect).filter_by(
                hashed_id=self.hashed_id
            ).first()
            mobile_redirect_instance = db.session.query(MobileRedirect).filter_by(
                hashed_id=self.hashed_id
            ).first()
        return desktop_redirect_instance, tablet_redirect_instance, mobile_redirect_instance
