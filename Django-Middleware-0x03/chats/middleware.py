from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        print("LOGGING:", log_entry.strip())  # <== Debug print

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Deny access if current time is between 9PM (21) and 6AM (6)
        if 21 <= current_hour or current_hour < 6:
            return HttpResponseForbidden("Access to chat is not allowed at this time.")
        return self.get_response(request)