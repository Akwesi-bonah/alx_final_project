#!/usr/bin/env python3
"""
auth
"""
import bcrypt
import uuid
from models.engine.db_storage import DBStorage as DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt
    Args:
    password (str): The password to hash

    Returns:
    bytes: The hashed password
    """
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID

    Returns:
        str: The string representation of the new UUID
    """
    # Generate a new UUID
    new_uuid = uuid.uuid4()

    # Return the string representation of the UUID
    return str(new_uuid)


class Auth:
    """auth class to interact with the authentication database.
    """
    def __init__(self):
        """ initialize """
        self._db = DB()

    def valid_login(self, cls, email: str, password: str) -> bool:
        """Validate login

        Args:
        email (str): The email of the user
        password (str): The password of the user

        Returns:
        bool: True if the password matches, False otherwise
        """
        try:
            # Locate the user by email
            user = self._db.find_by(cls, email=email)
            # Check the password
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, cls, email: str) -> str:
        """Create a new session for a user

        Args:
            email (str): The email of the user

        Returns:
            str: The new session ID
        """
        try:
            # Find the user corresponding to the email
            user = self._db.find_by(cls, email=email)
        except NoResultFound:
            return None

        # Generate a new UUID
        session_id = str(uuid.uuid4())

        # Store it in the database as the user's session_id
        self._db.update_by(user.id, cls, session_id=session_id)

        # Return the session ID
        return session_id

    def get_user_from_session_id(self, cls, session_id: str):
        """Get the user corresponding to a session ID

        Args:
            session_id (str): The session ID

        Returns:
            User: The corresponding User object, or None if no user is found
        """
        # If the session ID is None, return None
        if session_id is None:
            return None

        # Try to find the user with the given session ID
        try:
            user = self._db.find_by(cls, session_id=session_id)
        except NoResultFound:
            # If no user is found, return None
            return None

        # If a user is found, return the user
        return user

    def destroy_session(self,cls, user_id: int) -> None:
        """Destroy a user's session

        Args:
            user_id (int): The ID of the user

        Returns:
            None
        """
        # Update the user's session ID to None
        self._db.update_by(cls, user_id, session_id=None)

    def get_reset_password_token(self, cls, email: str) -> str:
        """Generate a reset password token for a user

        Args:
            email (str): The email of the user

        Returns:
            str: The reset password token

        Raises:
            ValueError: If no user exists with the given email
        """
        # Find the user corresponding to the email
        try:
            user = self._db.find_by(cls, email=email)
        except NoResultFound:
            # If the user does not exist, raise a ValueError
            raise ValueError()

        # If the user exists, generate a UUID
        reset_token = str(uuid.uuid4())

        # Update the user's reset_token database field
        self._db.update_by(cls, user.id, reset_token=reset_token)

        # Return the token
        return reset_token

    def update_password(self, cls, reset_token: str, password: str) -> None:
        """Update a user's password

        Args:
            reset_token (str): The reset password token
            password (str): The new password

        Raises:
            ValueError: If no user exists with the given reset token
        """
        # Find the user corresponding to the reset token
        try:
            user = self._db.find_by(cls, reset_token=reset_token)
        except NoResultFound:
            # If the user does not exist, raise a ValueError
            raise ValueError()

        # Update the user's hashed_password field with the new hashed password
        # and the reset_token field to None
        self._db.update_by(cls, user.id,
                             hashed_password=password,
                             reset_token=None)
