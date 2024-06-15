from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection

class UserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            redis_conn = get_redis_connection("default")
            user_key = f"user:{request.user.id}:online"
            redis_conn.set(user_key, True, ex=300)  # Set TTL to 5 minutes
