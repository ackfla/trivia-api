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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    def test_get_all_categories(self):
        """Test endpoint returns all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check for 200 response code
        self.assertEqual(data['success'], True) # Check json response includes success
        self.assertTrue(len(data['categories'])) # Check json response includes categories

    def test_get_paginated_questions(self):
        """Test endpoint returns paginated questions"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check for 200 response code
        self.assertEqual(data['success'], True) # Check json response includes success
        self.assertTrue(len(data['questions'])) # Check json response includes questions
        self.assertTrue(data['total_questions']) # Check json response includes total questions

    def test_get_404_paginated_questions(self):
        """Test endpoint returns 404 if page contains no questions"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) # Check for 404 response code
        self.assertEqual(data['success'], False) # Check json response includes false success
        self.assertEqual(data['message'], 'resource not found') # Check json response includes correct message

    def test_delete_question_by_id(self):
        """Test endpoint will delete a question by id"""
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200) # Check for 200 response code
        self.assertEqual(data['success'], True) # Check json response includes success
        self.assertEqual(data['deleted'], 2) # Check json response includes id of deleted question
        self.assertEqual(question, None) # Check question has been deleted

    def test_delete_question_by_non_exisiting_id(self):
        """Test endpoint will return not found for deleting a question by non existing id"""
        res = self.client().delete('/questions/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) # Check for 404 response code
        self.assertEqual(data['success'], False) # Check json response includes false success
        self.assertEqual(data['message'], 'resource not found') # Check json response includes correct message


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
