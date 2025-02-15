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


# Маппинг значений
FIELD_MAPPINGS = {
    "gender": {
        0: "Обрати",
        1: "Чоловік",
        2: "Жінка",
    },
    "yesNo": {
        0: "Ні",
        1: "Так",
    },
    "status": {
        0: "Працює",
        1: "Відпуска",
        2: "Звільнено",
        3: "Заблокований"
    },
    # Добавьте другие поля для маппинга здесь
}


def map_field_value(field_name, field_value):
    """
    Преобразует числовое значение поля в текстовое значение на основе маппинга.

    :param field_name: Название поля (ключ маппинга).
    :param field_value: Значение, которое нужно преобразовать.
    :return: Текстовое представление значения или оригинальное значение, если маппинг отсутствует.
    """
    return FIELD_MAPPINGS.get(field_name, {}).get(field_value, field_value)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def employee_list_view(request):
    period_start = request.data.get("period_start")
    period_end = request.data.get("period_end")

    with connection.cursor() as cursor:
        cursor.execute("""
SELECT m.mo_id,
       mp.name,
       m.name,
       m.live_start,
       m.live_end,
       m.hidden,
       m.description,
       m.auto_supertags,
       utm.live_start,
       utm.live_end,
       u.user_id,
       u.login,
       u.g_token,
       u.last_name,
       u.first_name,
       u.middle_name,
       u.sex,
       u.emp_code,
       u.photo,
       u.sms_phone,
       u.live_start,
       u.live_end,
       u.birthday,
       u.country,
       u.region,
       u.city,
       u.latitude,
       u.longitude,
       u.status,
       u.email,
       u.description,
       u.onesignal_id,
       u.layout_id,
       u.theme,
       rtu.role_id,
       ro.name,
       l.name,
       ma.name_alias,
       mh.since,
       mh.name,
       mh.consumers,
       mh.`order`,
       mh.hierarchy_path,
       mh.pid,
       CONCAT(u.last_name, ' ', UCASE(LEFT(u.first_name, 1)), '. ',
                        UCASE(LEFT(u.middle_name, 1)), '.') as initials
       
FROM mo m
         LEFT JOIN user_to_mo utm ON utm.mo_id = m.mo_id
            AND utm.live_end = (SELECT MAX(utm2.live_end) as max_live_end
                        FROM user_to_mo AS utm2
                        where m.mo_id = utm2.mo_id
                          and utm2.live_end >= %s
                          and utm2.live_start <= %s
                        group by utm2.mo_id)
         LEFT JOIN user u ON u.user_id = utm.user_id
         LEFT JOIN role_to_user rtu ON rtu.mo_id = m.mo_id
         LEFT JOIN role ro ON ro.role_id = rtu.role_id
         LEFT JOIN mo_position mp ON mp.mo_position_id = m.mo_position_id
         LEFT JOIN layouts l ON l.id = u.layout_id
         LEFT JOIN mo_hst mh ON mh.mo_id = m.mo_id
            AND mh.since = (SELECT MAX(mh2.since) as max_since
                    FROM mo_hst AS mh2
                    where mh2.mo_id = m.mo_id
                      AND mh2.since <= %s
                    group by mh2.mo_id)
         LEFT JOIN mo_aliases ma ON ma.mo_id = m.mo_id
where m.live_end >= %s
and m.live_start <= %s;
        """, [period_start, period_end, period_start, period_start, period_end])
        rows = cursor.fetchall()
        response_data = [
            {
                "mo_id": row[0],
                "mo_position": row[1],
                "name": row[2],
                "live_start": row[3],
                "live_end": row[4],
                "hidden": map_field_value("yesNo", row[5]),
                "description": row[6],
                "auto_supertags": row[7],
                "utm_live_start": row[8],
                "utm_live_end": row[9],
                "user_id": row[10],
                "login": row[11],
                # "g_token": row[12],
                "last_name": row[13],
                "first_name": row[14],
                "middle_name": row[15],
                "gender": map_field_value("gender", row[16]),
                "emp_code": row[17],
                "photo": row[18],
                "sms_phone": row[19],
                "u_live_start": row[20],
                "u_live_end": row[21],
                "birthday": row[22],
                "country": row[23],
                "region": row[24],
                "city": row[25],
                "latitude": row[26],
                "longitude": row[27],
                "status": map_field_value("status", row[28]),
                "email": row[29],
                "u_description": row[30],
                "onesignal_id": row[31],
                "layout_id": row[32],
                "theme": row[33],
                "role_id": row[34],
                "role_name": row[35],
                "layout_name": row[36],
                "mo_alias_name": row[37],
                "mo_hst_since": row[38],
                "mo_hst_name": row[39],
                "mo_hst_consumers": row[40],
                "mo_hst_order": row[41],
                "mo_hst_path": row[42],
                "mo_hst_pid": row[43],
                "initials": row[44],
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
