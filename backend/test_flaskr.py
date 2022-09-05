import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.trivia.models import Category, Question
from flaskr.trivia.models import setup_db
from flaskr.config import settings

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = settings.SQLALCHEMY_TEST_DATABASE_URI
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['success'])

    def test_get_paginated_questions(self):
        response = self.client().get('/questions?page=1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['success'])
        self.assertTrue(result["data"]["total_questions"]>0)
        self.assertIn('questions', result['data'].keys())

    def test_404_get_questions_beyond_valid_page(self):
        response = self.client().get('/questions?page=100')
        self.assertEqual(response.status_code, 404)


    def test_delete_question(self):
        question = {}
        with self.app.app_context():
            question = Question.query.first().format()
        response = self.client().delete(f"/questions/{question['id']}")
        self.assertEqual(response.status_code, 204)
        with self.app.app_context():
            quest = Question.query.filter(Question.id==question['id']).one_or_none()
            self.assertIsNone(quest)

    def test_404_delete_none_existing_question(self):
        max_id = 100000
        with self.app.app_context():
            q = Question.query.order_by(Question.id.desc()).first()
            if q:
                max_id = q.id
        response = self.client().delete(f"/questions/{max_id + 2}")
        self.assertEqual(response.status_code, 404)

    def test_new_question(self):
        data = {
            "question": "At what age did Micheal Jackson die?",
            "answer": "50",
            "category_id": 2,
            "difficulty": 2
        }
        response = self.client().post('/questions', json=data)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', result['data'].keys())

    def test_400_poorly_formatted_new_question_data(self):
        data = {
            "question": "At what age did Micheal Jackson die?",
            "answer": 50, # string expected, not integer
            "category_id": 2,
            "difficulty": 2
        }
        response = self.client().post('/questions', json=data)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(result['success'])

    def test_search_question_with_responses(self):
        response = self.client().post('/questions/search', json={'search_term': 'micheal'})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['data']['questions'])

    def test_search_questions_with_no_response(self):
        response = self.client().post('/questions/search', json={'search_term': 'abrakadabra'})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(result['data']['questions'])

    def test_get_questions_by_category(self):
        category = Category.query.first()
        with self.app.app_context():
            category = Question.query.first().category

        response = self.client().get(f"/categories/{category.id}/questions")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['success'])
        self.assertTrue(result['data']['questions'])
        self.assertEqual(result['data']['current_category'], category.format())

    def test_404_get_questions_by_category(self):
        category_id = 10000
        response = self.client().get(f"/categories/{category_id}/questions")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(result['success'])
        self.assertTrue(result['message'])


    def test_play_quiz_with_no_previous_question(self):
        category = {}
        with self.app.app_context():
            category = Question.query.order_by(self.db.func.random()).first().category.format()

        response = self.client().post(
            f'/quizzes',
            json={'quiz_category': category},
            headers={'Content-Type': 'application/json'}
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['success'])
        self.assertTrue(result['data'])

    def test_play_quiz_with_prev_question(self):
        question = {}
        quiz_category = {}
        with self.app.app_context():
           for cat in Category.query.all():
               if len(cat.questions) > 1:
                   question = cat.questions[0].format()
                   quiz_category = cat.format()
                   break

        response = self.client().post(
            f'/quizzes',
            json={'quiz_category': quiz_category, 'previous_questions': [question.get('id')]},
            headers={'Content-Type': 'application/json'}
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['success'])
        self.assertTrue(result['data'])

    def test_404_play_quiz_with_wrong_category(self):
        category = {}
        with self.app.app_context():
            category_id = Category.query.order_by(Category.id.desc()).first().id + 2
            category = {'id': category_id, "type": ""}

        response = self.client().post(f'/quizzes', json={'quiz_category': category})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(result['success'])

    def test_404_play_quiz_with_wrong_prev_question(self):
        question = {}
        with self.app.app_context():
            question = Question.query.order_by(Question.id.desc()).first()

        response = self.client().post(f'/quiz/{question.category_id}/{question.id + 2}')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(result['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()