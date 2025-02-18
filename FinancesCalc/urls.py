from django.urls import path
from django.views.generic import TemplateView
from rest_framework import permissions  # For permission settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import get_user_info, LoginView, employee_list_view, get_csrf_token, \
    manage_theme, set_option
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View


class GetCSRFTokenView(View):
    @ensure_csrf_cookie
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)


urlpatterns = [
    path('api/employees/', employee_list_view, name='employee_list_api'),  # API route for employee list
    path('api/login/', LoginView.as_view(), name='api_login'),  # API login route
    path('api/csrf-token/', get_csrf_token, name='get_csrf_token'),  # API for CSRF token
    path('api/options/', set_option, name='set_option'),
    path('api/theme/', manage_theme, name='manage_theme'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token route
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh route
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  # Homepage (React)
    path('<path:route>/', TemplateView.as_view(template_name='index.html'), name='react_routes'),  # React routes
]
