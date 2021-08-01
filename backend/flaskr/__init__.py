import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    '''
  App config
  '''
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Setup CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response

    '''
  Handle GET requests for all available categories.
  '''
    @app.route('/categories')
    def get_all_categories():

        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    '''
  Handle GET requests for questions, including pagination (every 10 questions).
  Returns a list of questions, number of total questions, current category, categories.
  '''
    @app.route('/questions')
    def get_all_questions():

        # Fetch all questions from db
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = [question.format() for question in questions]

        # Fetch all categories from db
        categories = Category.query.order_by(Category.id).all()
        formattedCategories = {
            category.id: category.type for category in categories}

        # Get page from request args object (1 as default)
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        current_questions = formatted_questions[start:end]

        # 404 if no questions
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': formattedCategories,
            'current_category': 1
        })

    '''
  DELETE question using a question ID.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        # Fetch question from db based on query parameter
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        # If no question found, return not found
        if question is None:
            abort(404)

        # Delete question
        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id,
        })

    '''
  POST a new question. Requires the question and answer text,
  category, and difficulty score.

  POST endpoint to get questions based on a search term.
  Returns any questions for whom the search term
  is a substring of the question.
  '''
    @app.route('/questions', methods=['POST'])
    def add_new_question_or_search():

        # Get JSON body
        body = request.get_json()
        # Get new question / search data
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        search = body.get('searchTerm', None)

        # Check for search term
        if search is not None:
            print(search)
            questions = Question.query.order_by(
                Question.id).filter(
                Question.question.ilike(
                    '%{}%'.format(search)))
            formattedQuestions = [question.format() for question in questions]
            return jsonify({
                'success': True,
                'questions': formattedQuestions,
                'total_questions': len(questions.all()),
                'current_category': 1
            })

        # Add new question
        else:
            try:
                # Add new question to db
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'total_questions': len(Question.query.all())
                })

            except BaseException:
                abort(422)

    '''
  GET endpoint to get questions based on category.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category_id(category_id):

        # Fetch category from db based on query parameter
        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        # If no category found, return not found
        if category is None:
            abort(404)

        # Fetch questions from db filtered by category name
        questions = Question.query.filter(
            Question.category == category_id).all()

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    '''
  @TODO:
  POST endpoint to get questions to play the quiz.
  Takes category and previous question parameters
  and returns a random question within the given category,
  if provided, and that is not one of the previous questions.
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        # Get JSON body
        body = request.get_json()

        # Get all quiz questions
        questions = Question.query

        if body['quiz_category']['id']:
            # Filter all questions by quiz category
            questions = questions.filter(
                Question.category == body['quiz_category']['id'])

        if body['previous_questions']:
            # Filter again to remove previous questions
            questions = questions.filter(
                Question.id.notin_(
                    body['previous_questions'])).all()

        # Check if any questions remaining
        if questions:
            # Format questions
            formattedQuestions = [question.format() for question in questions]
            # Pick a random one
            question = random.choice(formattedQuestions)

        # No questions are left
        else:
            question = False

        return jsonify({
            'success': True,
            'question': question
        })

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    return app
