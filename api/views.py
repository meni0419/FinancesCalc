from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import connection
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

from api.models import UserProfile


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


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM mo m
            left join user_to_mo utm on utm.mo_id = m.mo_id
            left join user u on u.user_id = utm.user_id
            left join role_to_user rtu ON rtu.mo_id = m.mo_id
        """)
        rows = cursor.fetchall()
        response_data = [
            {
                "mo_id": row[0],
#                "mo_type_id": row[1],
                "mo_position_id": row[2],
                "name": row[3],
                "live_start": row[4],
                "live_end": row[5],
                "hidden": row[6],
#                "tarif_id": row[7],
                "description": row[8],
                "auto_supertags": row[9],
#                "user_to_mo_id": row[10],
#                "utm_user_id": row[11],
#                "utm_mo_id": row[12],
                "utm_live_start": row[13],
                "utm_live_end": row[14],
                "user_id": row[15],
                "login": row[16],
                #"password": row[17],
                "g_token": row[18],
                "last_name": row[19],
                "first_name": row[20],
                "middle_name": row[21],
                "gender": row[22],
                "emp_code": row[23],
                "photo": row[24],
#                "hash": row[25],
                "sms_phone": row[26],
                "u_live_start": row[27],
                "u_live_end": row[28],
                "birthday": row[29],
#                "google": row[30],
                "country": row[31],
                "region": row[32],
                "city": row[33],
                "latitude": row[34],
                "longitude": row[35],
                "status": row[36],
#                "u_tarif_id": row[37],
                "email": row[38],
#                "blocked": row[39],
                "u_description": [40],
                "onesignal_id": row[41],
                "layout_id": row[42],
                "theme": row[43],
#                "id": row[44],
#                "role_to_user_id": row[45],
                "role_id": row[46],
#                "rtu_mo_id": row[47],
#                "rtu_user_id": row[48]
            }
            for row in rows
        ]
    return Response(response_data, status=200)


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
