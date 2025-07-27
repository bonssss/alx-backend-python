from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from collections import defaultdict
from threading import Lock
import time


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        print("LOGGING:", log_entry.strip())

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 21 <= current_hour or current_hour < 6:
            return HttpResponseForbidden("Access to chat is not allowed at this time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)
        self.lock = Lock()
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 60  # seconds

    def __call__(self, request):
        if request.method == "POST":
            ip_address = self._get_client_ip(request)
            current_time = time.time()

            with self.lock:
                # Keep only timestamps within the time window
                timestamps = self.ip_requests[ip_address]
                self.ip_requests[ip_address] = [
                    ts for ts in timestamps if current_time - ts < self.TIME_WINDOW
                ]

                if len(self.ip_requests[ip_address]) >= self.MESSAGE_LIMIT:
                    return JsonResponse(
                        {"error": "Message limit exceeded. Try again in a minute."},
                        status=429
                    )

                self.ip_requests[ip_address].append(current_time)

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        else:
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)