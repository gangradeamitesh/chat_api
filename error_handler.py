from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handler(app):

    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({
            "status":"error",
            'error': str(e.description) if e.description else 'Bad Request'
        }) , 400
    
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            'status': 'error',
            'error': 'Resource not found'
        }), 404
    
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        # Handle generic/unexpected exceptions
        if isinstance(e, HTTPException):
            return jsonify({
                'status': 'error',
                'error': str(e.description),
                'code': e.code
            }), e.code
            
        # Handle non-HTTP exceptions
        return jsonify({
            'status': 'error',
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500