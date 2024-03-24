#!/usr/bin/env python3
"""a module to manage the API authentication
"""
from sqlalchemy.exc import NoResultFound

from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models import  storage
from models.staff import Staff
from models.student import Student
from models.auth.auth import Auth as AuthModel


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns the Base64 part of the Authorization header'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(' ', 1)[1]
        return encoded

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''returns the decoded value of a Base64 string'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None
        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        '''returns the user email and password from the Base64 decoded value'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credential = decoded_base64_authorization_header.split(':', 1)
        return credential[0], credential[1]


    def staff_object_from_credentials(self, user_email: str, user_pwd: str) :
        '''Returns the User instance based on email and password'''

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        if not user_email.strip() or not user_pwd.strip():
            return None

        try:
            # Assuming User.search() returns a list of User objects

            get_users = storage.find_by(Staff, email=user_email)
            user = get_users.is_valid_password(user_pwd)
            if user:
                return user
            return None
        except Exception as e:
            print(f"An error occurred during user search: {e}")
            return None

    def student_object_from_credentials(self, user_email: str, user_pwd: str) :
            '''Returns the User instance based on email and password'''

            if not isinstance(user_email, str) or not isinstance(user_pwd, str):
                return None

            if not user_email.strip() or not user_pwd.strip():
                return None

            try:
                # Assuming User.search() returns a list of User objects

                get_users = storage.find_by(Student, email=user_email)
                user = get_users.is_valid_password(user_pwd)
                if user:
                    return user
                return None
            except Exception as e:
                print(f"An error occurred during user search: {e}")
                return None


    def current_user(self, request=None):
        '''overloads Auth and retrieves the User instance'''
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None
        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None
        try:
            user = self.staff_object_from_credentials(email, pwd)
        except NoResultFound as e:
            try:
                user = self.student_object_from_credentials(email, pwd)
            except NoResultFound as e:
                print(f"An error occurred during user search: {e}")
                return None

        return user



