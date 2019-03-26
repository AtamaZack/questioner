from rest_framework import status
from django.contrib.auth import login
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import ValidationError
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UserListSerializer)


class SignUp(APIView):
    """
    post:
    Register a user.
    """

    serializer_class = UserSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Create a user account.",
        operation_id="Sign up a user",
        request_body=UserSerializer,
        responses={201: UserSerializer(many=False), 400: "BAD REQUEST"},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except ValidationError as errors:
                return Response(
                        data={"status": 400,
                              "errors": [errors]
                              },
                        status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "data": [
                        {
                            "username": user.username,
                            "email": user.email,
                            "is_admin": user.is_superuser,
                        }
                    ],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"status": 400, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class Users(APIView):
    """
    Get:
    Lists all users
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwags):
        current_user = self.request.user
        if current_user.is_superuser:
            users = User.objects.all()
            serializer = UserListSerializer(users, many=True)

            return Response(data={"status": 200,
                            "data": serializer.data},
                            status=status.HTTP_200_OK
                            )

        return Response(data={"status": 403,
                        "error": "Insurfficient rights!"},
                        status=status.HTTP_403_FORBIDDEN
                        )


class Login(APIView):
    """
    post:
    login a user.
    """

    serializer_class = LoginSerializer

    @classmethod
    @swagger_auto_schema(
        operation_description="Login a User",
        operation_id="Login a user",
        request_body=UserSerializer,
        responses={200: UserSerializer(many=False), 401: "Invalid Login"},
    )
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.data['username'])
        login(request, user)

        return Response(
            data={"Username": serializer.data['username'],
                  "Email": serializer.data['email'],
                  "token": serializer.data['token']},
            status=status.HTTP_200_OK
        )


# accounts/profile/
class profile(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request):

        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(
            data={

                "status": status.HTTP_200_OK,
                "data": [
                    {

                        "user": {"Username": serializer.data['username'],
                                 "Email":serializer.data['email']}

                    }
                ],
            },
            status=status.HTTP_200_OK,
        )
