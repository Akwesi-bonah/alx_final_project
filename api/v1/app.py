#!/usr/bin/python3
""" API Blueprint"""
import smtplib
from os import getenv

from flask import Flask, make_response, jsonify, request, Response, abort
from flask_cors import CORS
from flasgger import Swagger
from api.v1.views import views
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': "Academy Haven Hostel Management System",
    'version': 1
}
Swagger(app)

AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(401)
def unauthorized(error) -> Response:
    """Unauthorized access error handler"""

    return make_response( jsonify({"error": "Unauthorized"}), 401)


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """  forbidden handler
    """
    return make_response( jsonify({"error": "Forbidden"}), 403)


@app.errorhandler(404)
def not_found(error) -> Response:
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


@app.errorhandler(smtplib.SMTPAuthenticationError)
def handle_smtp_authentication_error(error):
    return jsonify({'error': str(error)}), 500

#
# @app.before_request
# def before_request() -> str:
#     """ before_request handler
#     """
#     if auth is None:
#         return
#     excluded_paths = ['/api/v1/status/',
#                       '/api/v1/unauthorized/',
#                       '/api/v1/forbidden/',
#                       '/api/v1/student',
#                       ]
#     if not auth.require_auth(request.path, excluded_paths):
#         return
#     if auth.authorization_header(request) is None \
#             and auth.session_cookie(request) is None:
#         abort(401)
#     current_user = auth.current_user(request)
#     if current_user is None:
#         abort(403)
#     request.current_user = current_user

if __name__ == "__main__":
    """ Main function"""
    app.run(port=5003, debug=True)
