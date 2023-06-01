#!/usr/bin/env python3
"""SessionDBAuth."""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Store Session ID in database."""

    def create_session(self, user_id=None):
        """Create and stores new instance of UserSession."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID by requesting UserSession."""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user = UserSession.search({'session_id': session_id})

        if not user:
            return None

        user = user[0]
        start_time = user.created_at
        delta = timedelta(seconds=self.session_duration)
        print(start_time + delta)

        if (start_time + delta) < datetime.utcnow():
            return None
        return user.user_id

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID."""
        cookie = self.session_cookie(request)

        if cookie is None:
            return False

        if not self.user_id_for_session_id(cookie_data):
            return False

        user_session = UserSession.search({'session_id': cookie})

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return Fasle
        return True
