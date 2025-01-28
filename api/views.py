from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from api.models import UserProfile


def save_user_password(raw_password):
    hashed_password = make_password(raw_password)
    return hashed_password


def change_users_password():
    users = UserProfile.objects.all()
    for user in users:
        user.password = save_user_password(user.login)
        user.save()


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Validate credentials
        if user is not None:
            login(request, user)  # Login and create session
            return redirect('/employees/')  # Redirect on successful login
        else:
            # Re-render login page with an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')  # For GET requests, render login form


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if user exists and password matches
        try:
            user_profile = UserProfile.objects.get(login=username)
            if not check_password(password, user_profile.password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        refresh = RefreshToken.for_user(user_profile)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    # Query database for employee data
    employees = UserProfile.objects.all()
    employee_data = [
        {
            'id': emp.user_id,
            'first_name': emp.first_name,
            'middle_name': emp.middle_name,
            'last_name': emp.last_name,
            'email': emp.email,
        }
        for emp in employees
    ]
    return Response(employee_data)


@csrf_exempt  # Allow requests without CSRF token for simplicity (use cautiously in production)
@require_POST  # Ensure only POST requests are allowed

@swagger_auto_schema(
    method='post',  # Define the method for Swagger
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_ids': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                description="List of user IDs to fetch information for",
            ),
        },
        required=[],  # 'user_ids' is optional now
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,

                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'login': openapi.Schema(type=openapi.TYPE_STRING),
                    'middle_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'sms_phone': openapi.Schema(type=openapi.TYPE_INTEGER, format="int64"),
                    'emp_code': openapi.Schema(type=openapi.TYPE_STRING),
                    'photo': openapi.Schema(type=openapi.TYPE_STRING),
                    'sex': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'birthday': openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                    'country': openapi.Schema(type=openapi.TYPE_STRING),
                    'region': openapi.Schema(type=openapi.TYPE_STRING),
                    'city': openapi.Schema(type=openapi.TYPE_STRING),
                    'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                    'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'onesignal_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'theme': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        ),
        400: "Invalid JSON payload",
        404: "User not found",
    }
)
@api_view(['POST'])  # DRF API view decorator to handle POST requests
def get_user_info(request):
    try:
        # Extract JSON payload from the request
        body = request.data
        user_ids = body.get('user_ids', None)  # Extract 'user_ids' from the payload

        if user_ids is not None and not isinstance(user_ids, list):  # Validate that `user_ids` is a list if provided
            return Response({'error': 'Invalid data format. "user_ids" should be a list.'}, status=400)

        # Query your database to get user profiles
        if user_ids is None:
            users = UserProfile.objects.all()  # Retrieve all users if `user_ids` is not provided
        else:
            users = UserProfile.objects.filter(user_id__in=user_ids)

        # Collect user data into a list
        user_info_list = []
        for user in users:
            user_info_list.append({
                'id': user.user_id,
                'login': user.login,
                'middle_name': user.middle_name,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'sms_phone': user.sms_phone,
                'emp_code': user.emp_code,
                'photo': user.photo,
                'sex': user.sex,
                'birthday': user.birthday,
                'country': user.country,
                'region': user.region,
                'city': user.city,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'status': user.status,
                'description': user.description,
                'onesignal_id': user.onesignal_id,
                'theme': user.theme,
            })

        # Return the collected user information
        return Response(user_info_list)

    except UserProfile.DoesNotExist:
        return Response({'error': 'Some users not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
