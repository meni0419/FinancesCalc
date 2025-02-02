# File: api/middleware.py

class LogHeadersMiddleware:
    """
    Middleware to log all incoming request headers for debugging purposes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log all request headers
        print("Request Headers:", request.headers)

        # Call the next middleware or view
        response = self.get_response(request)

        return response