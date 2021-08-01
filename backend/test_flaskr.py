import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is 1+1?',
            'answer': '2!',
            'difficulty': 1,
            'category': 1
        }

        self.invalid_question = {
            'question': 'What is 1+1?',
            'anser': '2!',
            'difficulty': 1,
            'category': 1
        }

        self.previous_questions = {
            'previous_questions': [16, 17],
            'quiz_category': {
                'type': 'Art',
                'id': 2
            }
        }

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

    def test_get_all_categories(self):
        """Test endpoint returns all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response includes categories
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        """Test endpoint returns paginated questions"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response includes questions
        self.assertTrue(len(data['questions']))
        # Check json response includes total questions
        self.assertTrue(data['total_questions'])

    def test_get_404_paginated_questions(self):
        """Test endpoint returns 404 if page contains no questions"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Check for 404 response code
        # Check json response includes false success
        self.assertEqual(data['success'], False)
        # Check json response includes correct message
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question_by_id(self):
        """Test endpoint will delete a question by id"""
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response includes id of deleted question
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(question, None)  # Check question has been deleted

    def test_delete_question_by_non_exisiting_id(self):
        """Test endpoint will return not found for deleting a question by non existing id"""
        res = self.client().delete('/questions/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Check for 404 response code
        # Check json response includes false success
        self.assertEqual(data['success'], False)
        # Check json response includes correct message
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category_id(self):
        """Test endpoint will return questions belonging to a specific category"""
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response includes questions
        self.assertTrue(data['questions'])
        # Check json response includes total questions
        self.assertTrue(data['total_questions'])
        # Check json response includes correct category id
        self.assertEqual(data['current_category'], 2)

    def test_get_questions_by_invalid_category_id(self):
        """Test endpoint will return not found if invalid category id used"""
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)  # Check for 404 response code
        # Check json response includes false success
        self.assertEqual(data['success'], False)
        # Check json response includes correct message
        self.assertEqual(data['message'], 'resource not found')

    def test_add_new_question(self):
        """Test endpoint will add new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        question = Question.query.filter(
            Question.id == data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check question has been created
        self.assertTrue(question is not None)

    def test_405_if_question_creation_not_allowed(self):
        """Test endpoint will return 405 if invalid endpoint for new question used"""
        res = self.client().post('/questions/24', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)  # Check for 405 response code
        # Check json response includes false success
        self.assertEqual(data['success'], False)
        # Check json response includes correct message
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_questions_by_seach_term(self):
        """Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question."""
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response returns questions
        self.assertTrue(data['questions'])
        # Check json response returns total questions
        self.assertTrue(data['total_questions'])

    def test_get_random_question(self):
        """Test endpoint returns random question"""
        res = self.client().post('/quizzes', json=self.previous_questions)
        data = json.loads(res.data)
        print(data['question'])
        id = data['question']['id']

        self.assertEqual(res.status_code, 200)  # Check for 200 response code
        # Check json response includes success
        self.assertEqual(data['success'], True)
        # Check json response returns one of correct questions
        self.assertTrue(id == 18 or id == 19)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
