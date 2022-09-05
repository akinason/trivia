from typing import Dict
from flask import Blueprint, request, abort
from marshmallow import ValidationError

from flaskr import format_response
from flaskr.trivia.models import Question, Category, db
from flaskr.trivia.schema import QuestionSchema

bp = Blueprint('trivia', __name__, url_prefix='')

QUESTIONS_PER_PAGE = 10


def format_question_response(questions, total_questions, current_category) -> Dict:
    return {
        "questions": [q.format() for q in questions],
        "total_questions": total_questions,
        "current_category": current_category,
        "categories": [cat.format() for cat in Category.query.all()]
    }


"""
@TODO:
Create an endpoint to handle GET requests
for all available categories.
"""


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Category).order_by(Category.type).all()
    data = [cat.format() for cat in categories]
    return format_response(data, True, 200)


"""
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
"""


@bp.route('/questions', methods=['GET'])
def get_questions():
    page = int(request.args.get('page', 1))
    start = (page - 1) * QUESTIONS_PER_PAGE
    questions = Question.query.offset(start).limit(QUESTIONS_PER_PAGE).all()

    if len(questions) == 0:
        abort(404)

    data = format_question_response(
        questions,
        total_questions=Question.query.count(),
        current_category=''
    )
    return format_response(data, True, 200)


"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""


@bp.route('/questions/<id>', methods=['DELETE'])
def delete_question(id: int):
    question = Question.query.filter(Question.id == id).one_or_none()
    if question:
        question.delete()
        return format_response({}, True, 204)

    abort(404)


"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
# """


@bp.route('/questions', methods=['POST'])
def new_question():
    data = request.get_json()
    schema = QuestionSchema()

    try:
        data = schema.load(data)
    except ValidationError as e:
        abort(400)

    question = Question(**data)
    question.insert()
    return format_response(question.format(), True, 201)


"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
# """


@bp.route('/questions/search', methods=['POST'])
def search_question():
    search_term = request.get_json().get('search_term', '')
    questions = db.session.query(Question).filter(Question.question.ilike(f'%{search_term}%')).all()

    data = format_question_response(
        questions,
        total_questions=Question.query.count(),
        current_category=''
    )
    return format_response(data, True, 200)


"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""


@bp.route('/categories/<id>/questions', methods=['GET'])
def get_category_questions(id: int):
    category = Category.query.filter(Category.id == id).one_or_none()
    if category is None:
        abort(404)

    page = int(request.args.get('page', 1))
    start = (page - 1) * QUESTIONS_PER_PAGE
    questions = Question.query.filter(Question.category_id == id).offset(start).limit(QUESTIONS_PER_PAGE).all()

    data = format_question_response(
        questions,
        total_questions=Question.query.count(),
        current_category=Category.query.get(id).format()
    )
    return format_response(data, True, 200)


"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""


@bp.route('/quizzes', methods=['POST'])
def play_quiz_with_prev_question():
    quiz_category = request.get_json().get('quiz_category')
    previous_questions = request.get_json().get('previous_questions')

    category = Category.query.filter_by(id=quiz_category.get('id')).one_or_none()
    if category is None:
        abort(404)

    query = Question.query.filter(Question.category_id == category.id)
    if previous_questions:
        query = query.filter(Question.id.notin_(previous_questions))

    question = query.order_by(db.func.random()).first()

    if not question:
        abort(404)

    return format_response(question.format(), True, 200)


"""
@TODO:
Create error handlers for all expected errors
including 404 and 422.
"""
