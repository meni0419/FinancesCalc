from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from api.models import UserProfile


@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('/login/')  # Failed login

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        response = redirect('/employees/')
        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            max_age=3600,  # 1 hour expiration
            httponly=False,  # Allow access from JavaScript
            samesite='Lax',  # Adjust as needed based on your environment
        )
        response.set_cookie(
            'refresh_token',
            str(refresh),
            max_age=3600 * 24 * 30,  # 30 days expiration
            httponly=False,
            samesite='Lax',
        )
        return response

    return render(request, 'login.html')


class LoginView(APIView):
    """
      Login API to authenticate user and return JWT tokens.
      """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Serialize all fields in the UserProfile model


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    try:
        # Validate token automatically via IsAuthenticated permission
        employees = UserProfile.objects.all()
        serializer = UserProfileSerializer(employees, many=True)
        return Response(serializer.data)  # Return employee data as JSON
    except InvalidToken:
        return Response({'error': 'Invalid or expired token'}, status=401)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    #     })def employee_list_view(request):
    # try:
    #     # Check for the token in the Authorization header
    #     auth_header = request.META.get("HTTP_AUTHORIZATION", None)
    #
    #     # If the token is not in the header, check the cookies
    #     if not auth_header:
    #         access_token = request.COOKIES.get('access_token')
    #         if access_token:
    #             auth_header = f"Bearer {access_token}"
    #
    #     if not auth_header:
    #         return render(request, 'employee_list.html', {
    #             'error': 'Authorization header missing'
    #         })
    #
    #     # Validate token
    #     raw_token = auth_header.split()[-1]  # Extract token from "Bearer <TOKEN>"
    #     token = JWTAuthentication().get_validated_token(raw_token)
    #
    #     # If token is valid, proceed with fetching employees
    #     employees = UserProfile.objects.all()
    #     serializer = UserProfileSerializer(employees, many=True)
    #
    #     # Pass employee data to the template
    #     return render(request, 'employee_list.html', {'employees': serializer.data})
    #
    # except InvalidToken as e:
    #     print(f"Token validation failed: {e}")  # Debugging logs
    #     return render(request, 'employee_list.html', {
    #         'error': 'Invalid or expired token'
    #     })
    # except Exception as e:
    #     print(f"Unexpected error: {e}")  # Debugging logs
    #     return render(request, 'employee_list.html', {
    #         'error': 'An error occurred'
    #     })


@api_view(['POST'])
def logout_view(request):
    """
    Clears tokens by removing cookies.
    """
    response = Response({"detail": "Logged out successfully."}, status=204)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


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
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Fetches detailed information of users based on provided user IDs or retrieves all users if no IDs are specified.

    :param request: The HTTP request object containing JSON payload with optional 'user_ids'.
    :return: JSON response of user data or error messages.
    """
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


def auto_create_user_profiles():
    """
    Automatically creates user accounts for all profiles in the UserProfile model.
    Links the profiles to the created users if not already linked.
    """
    for profile in UserProfile.objects.all():
        user, created = User.objects.get_or_create(
            username=profile.login,
            defaults={
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
                'password': profile.password,
            }
        )
        profile.user = user
        profile.save()


def save_user_password(raw_password):
    """
    Hashes a given plaintext password using Django's hashing framework.

    :param raw_password: The plaintext password to be hashed.
    :return: The hashed password.
    """
    hashed_password = make_password(raw_password)
    return hashed_password


def change_users_password():
    """
    Update all user passwords in the UserProfile model by hashing their login as the password.
    """
    users = UserProfile.objects.all()
    for user in users:
        user.password = save_user_password(user.login)
        user.save()
