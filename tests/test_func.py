from tests.base import BaseTestCase
import json


class TestShortUrlGeneration(BaseTestCase):
    # 测试新建一个短链接
    def test_shorten_with_new_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = {
            'url': 'www.google.com'
        }
        response = self.client.post('/shorten', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_shorten_with_none(self):
        data = {
            'url': ''
        }
        response = self.client.post('/shorten', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_real_url(self):
        response = self.client.get('/0aaaaa')
        self.assertEqual(response.status_code, 302)
