from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='email already in use')
                    ],

    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='username already in use')
                    ],
    )
    password = serializers.CharField()

    @classmethod
    def create(cls, validated_data):
        validate_password(validated_data["password"],
                          user=None,
                          password_validators=None)

        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer to return user listing without critical information
    """

    class Meta:
        model = User
        fields = ("id",
                  "username",
                  "email",
                  "first_name",
                  "last_name",
                  "is_staff",
                  "is_active",
                  "is_superuser",
                  "last_login",
                  "date_joined"
                  )


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "token", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    @classmethod
    def validate(cls, data):
        user_obj = None
        username = data.get("username", None)
        password = data.get("password", None)

        if not username:
            raise serializers.ValidationError(
                "Username or email is required to login")

        user = User.objects.filter(
            Q(email=username) | Q(username=username)).distinct()
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("Invalid Username/Email")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError(
                    "Incorrect credentials please try again")

        data["token"] = Token.objects.get_or_create(user=user_obj)[0].key
        data["email"] = user_obj.email

        return data
