from datetime import datetime
from django.http import HttpResponse

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
        current_time = datetime.now().time()
        start_time = datetime.strptime("08:00", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        if not (start_time <= current_time <= end_time):
            return HttpResponse("Access restricted to business hours (08:00 - 18:00).", status=403)

        return self.get_response(request)
