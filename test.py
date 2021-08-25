from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def setUp(self):
        """ Set up test client """
        self.client = app.test_client()

    def test_homepage(self):
        """ Test home page html information and session"""
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Your highscore: 0 in 0 plays", html)

    def test_check_word_json(self):
        """ Test valid, invalid and non-english word"""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [['U', 'F', 'N', 'D', 'B'],
                                           ['S', 'I', 'A', 'A', 'L'],
                                           ['O', 'V', 'X', 'R', 'E'], 
                                           ['S', 'X', 'D', 'O', 'Q'], 
                                           ['X', 'C', 'A', 'E', 'X']]
    
            res = self.client.get('/check-word/json?word=adorable')
            self.assertEqual(res.json['result'], 'ok')

            res2 = self.client.get('/check-word/json?word=asfasdfa')
            self.assertEqual(res2.json['result'],'not-word')

            res3 = self.client.get('/check-word/json?word=flower')
            self.assertEqual(res3.json['result'],'not-on-board')

    def test_calculate_score(self):
        """ Test calculate score and html information """

        with self.client as client:
            with client.session_transaction() as change_session:
                change_session["highscore"] = 5

            
            res = self.client.post("/final-score", 
                       data=json.dumps(dict(score=10)),
                       content_type='application/json')


            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['brokeRecord'], True)

            res2 = self.client.get('/')
            html = res2.get_data(as_text=True)
            self.assertIn("Your highscore: 10 in 1 plays", html)


        



    

