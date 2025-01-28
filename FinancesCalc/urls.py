from django.urls import path
from rest_framework import permissions  # For permission settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from api.views import get_user_info, LoginView, employee_list_view, login_page, logout_view  # Import your view
from django.shortcuts import redirect
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="My API Documentation",  # The title of your API documentation
        default_version="v1",  # API version
        description="API documentation for our project",  # Brief description
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),  # Change this to your support email
        license=openapi.License(name="BSD License"),  # Optional license information
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Allow all users to access the docs
)


def home_page(request):
    """
    Redirects to login or employees list based on token validity.
    """
    # Check for the access token in the cookies
    token = request.COOKIES.get('access_token')

    if not token:
        return redirect('/login/')  # Redirect to login if no token is present

    try:
        # Validate the token using SimpleJWT
        JWTAuthentication().get_validated_token(token)
        return redirect('/employees/')  # Redirect to employees page if the token is valid
    except AuthenticationFailed:
        return redirect('/login/')  # Redirect to login if the token is invalid


urlpatterns = [
    path('', home_page, name='home'),
    path('employees/', employee_list_view, name='employee_list'),
    path('logout/', logout_view, name='logout'),
    # Your existing paths
    path('user-info/', get_user_info, name='get_user_info'),
    path('api/login/', LoginView.as_view(), name='api_login'),  # REST API login
    path('login/', login_page, name='login_page'),  # HTML login page
    path('employees/', employee_list_view, name='employee_list'),  # Employee list for authorized users
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
