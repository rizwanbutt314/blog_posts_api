import json
from app.test.base import BaseTestCase


class TestAPIPing(BaseTestCase):

    def test_ping_api(self):
        response = self.client.get('/api/ping', headers={"Content-Type": "application/json"})
        api_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(api_data['success'])
        self.assertTrue(api_data['success'])
