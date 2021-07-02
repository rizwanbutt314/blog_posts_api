from flask_testing import TestCase

from manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass
