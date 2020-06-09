import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    # Sets pagination of 10 questions per page.
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Formats the questions.
    questions = [question.format() for question in selection]
    # Selects only 10 questions from start to end.
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # Creates and configures the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        # Sets access control for headers and methods.
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/questions/<int:question_id>', methods=['PATCH'])
    def update_question(question_id):
        # Handles PATCH requests for updating a question's category by id.

        # Gets information from the request.
        body = request.get_json()

        # Retrieves question from the database by id.
        question = Question.query.filter_by(id=question_id).one_or_none()

        # Aborts if no question was found.
        if question is None:
            abort(404)

        # Sets and updates the question's category.
        question.category = body.get('category')
        question.update()

        # Returns data.
        return jsonify({
            'success': True,
            'question_id': question.id
        })

    @app.route('/categories')
    def get_categories():
        # Handles GET requests for all available categories.
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for
                                category in categories}

        # Aborts if there is no categories found.
        if(len(formatted_categories) == 0):
            abort(404)

        # Returns data.
        return jsonify({
          'success': True,
          'categories': formatted_categories
        })

    @app.route('/questions')
    def get_questions():
        # Handles GET requests for all questions.

        # Gets page number from request.
        body = request.args.get('page', None, int)

        # Aborts if page is not provided.
        if(body is None):
            abort(400)

        # Retrieves the questions paginated.
        questions = Question.query.all()
        current_questions = paginate(request, questions)

        # Aborts if no questions are found.
        total_num_of_questions = len(current_questions)
        if (total_num_of_questions == 0):
            abort(404)

        # Retrieves the categories formatted.
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for
                                category in categories}

        # Aborts if there is no categories found.
        if(len(formatted_categories) == 0):
            abort(404)

        # Returns data.
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all()),
          'categories': formatted_categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # Handles DELETE requests for deleting questions.
        try:
            # Retrieves a question by its ID.
            question = Question.query.filter_by(id=question_id).one_or_none()

            # Aborts if question is not found.
            if question is None:
                abort(404)
            else:
                # Deletes question.
                question.delete()

                # Returns data.
                return jsonify({
                    'success': True,
                    'deleted_question': question.format(),
                    'total_num_of_questions': len(Question.query.all())
                })
        # Aborts if an exception is caught.
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        # Handles POST requests for adding new questions.

        # Gets the request's body.
        body = request.get_json()

        # Aborts if request body was empty.
        if body is None:
            abort(400)

        # Gets the request's question information.
        question_name = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        # Aborts if any of the fields are empty.
        if ((question_name is None) or (answer is None)
                or (difficulty is None) or (category is None)):
            abort(400)

        try:
            # Creates a new question.
            question = Question(question=question_name,
                                answer=answer,
                                category=category,
                                difficulty=difficulty)
            # Inserts a new question.
            question.insert()

            # Returns data.
            return jsonify({
                'success': True,
                'total_num_of_questions': len(Question.query.all()),
                'created_question': question.format()
            })

            # Aborts if an exception is caught.
        except Exception:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        # Handles POST requests for searching questions.

        # Gets the request's body.
        body = request.get_json()

        # Aborts if request body was empty.
        if body is None:
            abort(400)

        # Gets the search term from the request.
        search_term = body.get('searchTerm')

        # Queries the database by the search term, case-insensitive.
        questions = Question.query.filter(
                Question.question.ilike('%' + search_term + '%')).all()

        # Aborts if no results are found.
        if (len(questions) == 0):
            abort(404)

        # Retrieves the questions paginated.
        current_questions = paginate(request, questions)

        # Returns data.
        return jsonify({
             'success': True,
             'total_questions': len(questions),
             'questions': current_questions
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # Handles GET requests to get all questions by category.

        if category_id == 0:
            # Retrieves all questions.
            questions = Question.query.all()
        else:
            # Retrieve category information.
            category = Category.query.filter_by(id=int(category_id)).one_or_none()

            # Abort if category is not found.
            if category is None:
                abort(404)

            # Retrieves all questions by a specific category.
            questions = Question.query.filter_by(
                category=str(category.id)).all()

        # Retrieves the questions paginated.
        current_questions = paginate(request, questions)

        # Returns data.
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(questions),
          'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        # Handles POST requests to get random questions to play the quiz.

        # Gets information from the request.
        body = request.get_json()
        previous_questions = body.get('previousQuestions')
        category = body.get('quizCategory')['id']

        # Aborts if any of the parameters are empty.
        if((previous_questions is None) or (category is None)):
            abort(400)

        # Retrieves all questions that are not in previous_questions.
        questions = Question.query.filter(
            Question.id.notin_(previous_questions)).all()

        # Retrieves all questions by a specific category.
        if(category != 0):
            questions = Question.query.filter(
                Question.category == str(category)).filter(
                    Question.id.notin_(previous_questions)).all()

        # Aborts if no questions were found.
        if(len(questions) == 0):
            return jsonify({
              'success': False,
              'question': False
            })

        # Selects a random question from the list of retrieved questions.
        random_question = questions[random.randrange(0,
                                    len(questions), 1)].format()

        # Returns data.
        return jsonify({
          'success': True,
          'question': random_question
        })

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad Request.'
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource not found.'
        }), 404

    @app.errorhandler(422)
    def unprocessable_error(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unprocessable entity.'
        }), 422

    return app
