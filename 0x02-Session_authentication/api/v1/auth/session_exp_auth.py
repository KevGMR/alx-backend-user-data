#!/usr/bin/env python3
"""Session Expiration Auth Module
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Expiration Authentication class
    """
    def __init__(self):
        """Initialization
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID
        Args:
            user_id: user id
        Returns:
            session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method to return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        val = self.user_id_by_session_id.get(session_id)
        if not val:
            return None
        user_id = val.get('user_id')
        creation_time = val.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if creation_time is None:
            return None

        now = datetime.now()
        live_time = timedelta(seconds=self.session_duration)

        if now > creation_time + live_time:
            return None

        return user_id
