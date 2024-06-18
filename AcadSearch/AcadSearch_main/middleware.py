import logging
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                redis_conn = get_redis_connection("default")
                user_key = f"user:{request.user.username}:online"
                redis_conn.set(user_key, "true", ex=300)  # Set value as a string
                logger.info(f"User activity updated for user: {request.user.username}")
            except Exception as e:
                logger.error(f"Error updating user activity for user: {request.user.username} - {e}")
