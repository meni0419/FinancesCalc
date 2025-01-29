from django.urls import path
from django.views.generic import TemplateView
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


# def home_page(request):
#     """
#     Redirects to /login/ or /employees/ based on token validity.
#     """
#     token = request.COOKIES.get('access_token')
#     if not token:
#         # If no token exists, render the login page, not redirect
#         return redirect('/login/')  # Change to render in standalone HTML if needed
#     try:
#         JWTAuthentication().get_validated_token(token)
#         return redirect('/employees/')
#     except AuthenticationFailed:
#         return redirect('/login/')



urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('employees/', TemplateView.as_view(template_name='index.html'), name='employee_list'),  # React route
    path('api/employees/', employee_list_view, name='employee_list_api'),  # Employee list for authorized users
    path('logout/', logout_view, name='logout'),
    # Your existing paths
    path('user-info/', get_user_info, name='get_user_info'),
    path('api/login/', LoginView.as_view(), name='api_login'),  # REST API login
    path('login/', login_page, name='login_page'),  # HTML login page
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
