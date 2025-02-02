# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.authentication import BaseAuthentication
#
#
# class CookieJWTAuthentication(BaseAuthentication):
#     """
#        Custom authentication class that checks for JWT tokens in cookies.
#        """
#
#     def authenticate(self, request):
#         # Check if the Authorization header is present
#         auth_header = request.META.get("HTTP_AUTHORIZATION", None)
#         if auth_header:
#             # If the header is present, let DRF handle it
#             return None
#
#         # If no Authorization header, try fetching token from cookies
#         token = request.COOKIES.get('access_token')
#         if not token:
#             return None  # No token found in cookies, return None for DRF to continue
#
#         # Validate the token using SimpleJWT's logic
#         try:
#             validated_token = JWTAuthentication().get_validated_token(token)
#             return JWTAuthentication().get_user(validated_token), validated_token
#         except InvalidToken:
#             raise AuthenticationFailed("Invalid or expired token.")
