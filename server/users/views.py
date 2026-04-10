# ================= MODELS =============
from users.models import User, UserConfirmation, AuthStatus, AuthType

# ================= Dango ===============
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render

# ================= REST FRAMEWORK ======
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

# ================ SERIALIZERS =========
from .serializers import (
    SignUpSerializer,
    VerifyCodeSerializer,
    UpdateUserSerializer,
    UploadAvatarSerializer,
    LoginSerializer,
    ForgetPasswordSerializer,
    UpdatePasswordSerializer,
)

# ================ SHARED ================
from shared.utility import send_email

# =============== TOKENS =================
from .tokens import RegsitrationToken

# ================ AUTHHORZATIONS ========
from .authentication import RegistrationTokenAuthentication

# ================ PERMISITIONS ==========
from .permissions import IsRegistrationToken, CanVerifyCodeSend, CanSetUsernamePasssword


class SignUpView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class VerifyCodeView(APIView):
    authentication_classes = [RegistrationTokenAuthentication]
    permission_classes = [IsRegistrationToken, CanVerifyCodeSend]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        user: User = self.request.user

        user_confirmation: UserConfirmation = UserConfirmation.objects.filter(
            user=user, code=code, expired_time__gt=timezone.now(), is_confirmed=False
        ).first()

        if not user_confirmation:
            raise ValidationError("Invalid code")

        with transaction.atomic():
            user.auth_status = AuthStatus.VERIFIED
            user.save(update_fields=["auth_status"])

            user_confirmation.is_confirmed = True
            user_confirmation.save(update_fields=["is_confirmed"])

        token = RegsitrationToken.for_user(user)

        return Response(
            {
                "success": True,
                "data": {
                    "update_user_token": str(token),
                    "auth_status": AuthStatus.VERIFIED,
                },
            },
            status=status.HTTP_200_OK,
        )


class UpdateVerifyCode(APIView):

    authentication_classes = [RegistrationTokenAuthentication]
    permission_classes = [IsRegistrationToken, CanVerifyCodeSend]

    def post(self, request):

        user: User = self.request.user

        user_confirmation: bool = UserConfirmation.objects.filter(
            user=user, expired_time__gt=timezone.now()
        ).exists()

        if user_confirmation:
            raise ValidationError("you have got valid code . Please wait")

        if user.auth_type == AuthType.VIA_EMAIL:
            code = user.create_code(AuthType.VIA_EMAIL)
            email = user.email
            send_email(code=code, email=email)
        elif user.auth_type == AuthType.VIA_PHONE:
            phone_number = user.phone_number
            code = user.create_code(AuthType.VIA_PHONE)
            send_email(phone_number, code)
        else:
            raise ValidationError("SERVER error")

        return Response(
            {"success": True, "message": "send verify code to your email address"}
        )


class UpdateUserView(generics.UpdateAPIView):

    authentication_classes = [RegistrationTokenAuthentication]
    permission_classes = [IsRegistrationToken, CanSetUsernamePasssword]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        print("=" * 50)
        print(self.request.user)
        print("=" * 50)
        return self.request.user


class UploadAvatarView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadAvatarSerializer

    def get_object(self):
        return self.request.user


class LogOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            user: User = self.request.user
            user.auth_status = AuthStatus.NEW
            user.save()
            return Response(
                {"success": True, "message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token or token already blacklisted."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]

        token = user.token()

        return Response({**serializer.data, "tokens": token})


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = serializer.validated_data["user"]

        token = RegsitrationToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "We have sent you a verification code",
                "tokens": str(token),
            }
        )


class UpdatePasswordView(APIView):
    authentication_classes = [RegistrationTokenAuthentication]
    permission_classes = [IsRegistrationToken, CanSetUsernamePasssword]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]
        user: User = self.request.user

        user.set_password(new_password)
        user.save()
        return Response(
            {
                "success": True,
                "message": "Password successfuly update",
            },
            status=status.HTTP_200_OK,
        )
