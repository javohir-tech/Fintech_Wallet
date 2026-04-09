# ================= MODELS =============
from users.models import User, UserConfirmation, AuthStatus

# ================= Dango ===============
from django.utils import timezone
from django.shortcuts import render

# ================= REST FRAMEWORK =====
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

# ================ SERIALIZERS =========
from .serializers import SingUpSerializer


class SingUpView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = SingUpSerializer
    permission_classes = [AllowAny]


class VerifyCodeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        if "code" not in data:
            raise ValidationError("Invalid proporty")

        code: str = data["code"]

        if not code.isdigit() or len(code) != 4:
            raise ValidationError("Invalid code")

        user: User = self.request.user

        user_confirmation: UserConfirmation = UserConfirmation.objects.filter(
            user=user, code=code, expired_time__gt=timezone.now() , is_confirmed = False
        ).first()

        if not user_confirmation:
            raise ValidationError("Invalid code")

        user.auth_status = AuthStatus.VERIFIED
        user.save(update_fields=["auth_status"])

        user_confirmation.is_confirmed = True
        user_confirmation.save(update_fields=["is_confirmed"])

        token = user.token()

        return Response(
            {
                "success": True,
                "data": {
                    "access_token": token["access_token"],
                    "refresh_token": token["refresh_token"],
                    "auth_type": AuthStatus.VERIFIED,
                },
            },
            status=status.HTTP_200_OK,
        )


# Create your views here.
