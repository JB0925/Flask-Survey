from re import S, T
from unittest import TestCase
from urllib.parse import urlparse
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(topdir)
from app import app


class TestSurveyRoutes(TestCase):
    def test_home_get_request(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button type="submit">Start Survey</button>', html)
    

    def test_home_post_request(self):
        with app.test_client() as client:
            resp = client.post('/')
            self.assertIn('302' or '304', str(resp.status_code))
            self.assertNotEqual(resp.status_code, 200)
    

    def test_intermediary_route(self):
        with app.test_client() as client:
            resp = client.post('/test')
            self.assertEqual(resp.status_code, 302)
        
        with app.test_client() as client:
            resp = client.get('/test')
            self.assertEqual(resp.status_code, 405)
    

    def test_redirect_to_thanks_route(self):
        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['responses'] = []
                for i in range(4):
                    answers = sesh['responses']
                    answers.append(i)
                    sesh['responses'] = answers
            
            resp = client.post('/questions/3')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(urlparse(resp.location).path, '/thanks')
    

    def test_questions_routes(self):
        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['responses'] = []

            resp = client.get('/questions/0')
            self.assertEqual(resp.status_code, 200)
            resp = client.get('/questions/5')
            self.assertEqual(resp.status_code, 302)
            resp = client.get('/questions/-4')
            self.assertEqual(resp.status_code, 302)
            resp = client.get('/questions/1.3')
            self.assertEqual(resp.status_code, 302)
            resp = client.get('/questions/32')
            self.assertEqual(resp.status_code, 302)

            with client.session_transaction() as sesh:
                sesh['responses'] = ['yes', 'no']
            
            resp = client.get('/questions/10')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(urlparse(resp.location).path, '/questions/2')
    

    def test_thanks_route(self):
        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['responses'] = ['yes', 'no', 'maybe so', 'hahaha']

            resp = client.get('/thanks')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Thank you for taking our survey.</h1>', resp.get_data(as_text=True))

            post_resp = client.post('/thanks')
            self.assertEqual(post_resp.status_code, 405)
