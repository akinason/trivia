from typing import Any
from flask import Flask, jsonify
from flask_cors import CORS
from flaskr.trivia.models import setup_db, db
from flask_migrate import Migrate


def format_response(data: Any, success: bool, status_code: int = 200, message: str = "") -> jsonify:
    return jsonify({
        "success": success,
        "data": data,
        "message": message,
        "status_code": status_code
    }), status_code


migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # print('database engine: ', app.db.get_engine())
    CORS(app)
    migrate.init_app(app, db)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Methods'] =  '*'
        response.headers['Access-Control-Allow-Origins'] = '*'
        return response

    """
    Error Handlers
    """
    @app.errorhandler(400)
    def bad_request_error(error):
        return format_response(
            {}, False, 400,
            message="The request body was not properly formatted."
        )

    @app.errorhandler(404)
    def not_found_error(error):
        return format_response(
            {}, False, 404,
            message="The resource you are looking for does not exist."
        )

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return format_response(
            {}, False, 405,
            message="The HTTP method used is not allowed for this route."
        )

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return format_response(
            {}, False, 422,
            message="Unprocessable entity."
        )

    # Register blueprints
    from flaskr.trivia.views import bp as trivia_bp
    app.register_blueprint(trivia_bp)

    return app

