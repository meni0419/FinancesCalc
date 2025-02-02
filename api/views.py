from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserProfile, Mo, UserToMo


def get_csrf_token(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrfToken": csrf_token})
    response.set_cookie('csrftoken', csrf_token)  # Устанавливаем CSRF-токен в куки
    return response


class LoginView(APIView):
    # Allow unauthenticated access
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens for authenticated user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # Explicitly list all fields except the 'password' field
        fields = [
            'id', 'login', 'middle_name', 'first_name', 'last_name', 'email', 'sms_phone',
            'emp_code', 'photo', 'sex', 'birthday', 'country', 'region', 'city', 'latitude',
            'longitude', 'status', 'description', 'onesignal_id', 'theme'
        ]


class MoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mo
        fields = '__all__'


class UserToMoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToMo
        fields = '__all__'


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    employees = UserProfile.objects.all()
    mo_objects = Mo.objects.all()

    employee_serializer = UserProfileSerializer(employees, many=True)
    mo_serializer = MoSerializer(mo_objects, many=True)

    return Response(mo_serializer.data, status=200)


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
