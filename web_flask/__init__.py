#!/usr/bin/python3
"""
flask setup
"""
import os

from flask import Flask, render_template
from web_flask.componet.views import staff_view
from web_flask.student_model import student_views
from flask_session import Session


def create_app():
    app = Flask(__name__)
    # database connection
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_COOKIE_NAME'] = 'staff_session'
    app.config['STUDENT_SESSION_COOKIE_NAME'] = 'student_session'
    # Session configurations
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    app.config['SESSION_KEY_PREFIX'] = 'session:'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    app.config['PAYSTACK_SECRET_'] = 'sk_test_7530309aeb43b700e14cf312de735ad407747903'
    app.config['PAYSTACK_PUBLIC_KEY'] = 'pk_test_4ccdf50310beaaefdde4febbcef5fee8fbbd7011'
    app.register_blueprint(staff_view, url_prefix='/staff/')
    app.register_blueprint(student_views, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # @app.errorhandler(Exception)
    # def unhandled_exception(e):
    #     return render_template('error.html',
    #                            error=str(e)), 500

    if __name__ == '__main__':
        app.run(debug=True)


    return app
