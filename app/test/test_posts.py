import json
import mock

from app.test.base import BaseTestCase
from app.main.utils.helpers import sort_list_of_objects

posts_test_data = [
    {"author": "Lainey Ritter", "authorId": 1, "id": 96, "likes": 395, "popularity": 0.44, "reads": 99575,
     "tags": ["science", "history"]},
    {"author": "Jaden Bryant", "authorId": 3, "id": 51, "likes": 487, "popularity": 0.01, "reads": 98798,
     "tags": ["design", "startups", "tech"]}, ]


class TestPosts(BaseTestCase):

    @mock.patch('app.main.controller.blog_posts.get_tags_based_posts',
                return_value=posts_test_data)
    def test_posts_api(self, mocked_hatchways_api):
        # Without any query param
        response = self.client.get('/api/posts')

        api_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(api_data['error'], "Tags parameter is required")

        # With invalid sortBy value
        response = self.client.get('/api/posts', query_string={"tags": "123", "sortBy": "123123"})

        api_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(api_data['error'], "sortBy parameter is invalid")

        # With valid sortBy value and invalid direction
        response = self.client.get('/api/posts', query_string={"tags": "123", "sortBy": "id", "direction": "abc"})

        api_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(api_data['error'], "direction parameter is invalid")

        # With valid query param tag
        response = self.client.get('/api/posts', query_string={"tags": "123"})

        api_data = json.loads(response.data.decode())
        sorted_data = sort_list_of_objects(api_data['posts'], 'id', 'asc')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(api_data['posts']), 2)

        # With valid query params tags,sortBy,direction to test sorting in ascending order
        response = self.client.get('/api/posts', query_string={"tags": "123", "sortBy": "id", "direction": "asc"})

        api_data = json.loads(response.data.decode())
        sorted_data = sort_list_of_objects(api_data['posts'], 'id', 'asc')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_data['posts'][0]['id'], sorted_data[0]['id'])

        # With valid query params tags,sortBy,direction to test sorting in descending order
        response = self.client.get('/api/posts', query_string={"tags": "123", "sortBy": "id", "direction": "desc"})

        api_data = json.loads(response.data.decode())
        sorted_data = sort_list_of_objects(api_data['posts'], 'id', 'desc')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(api_data['posts'][0]['id'], sorted_data[0]['id'])

        mocked_hatchways_api.assert_called()
        mocked_hatchways_api.reset_mock()
