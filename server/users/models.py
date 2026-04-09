# ==================== PYTHON =========================
import uuid
from random import randint
from datetime import timedelta

# ==================== SHARED =========================
from shared.models import BaseModel

# ==================== DJANGO =========================
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import identify_hasher

# ==================== REST FRAMEWORK ==================
from rest_framework_simplejwt.tokens import RefreshToken


def is_hashing(password):
    try:
        identify_hasher(password)
        return True
    except Exception:
        return False


class AuthStatus(models.TextChoices):
    NEW = "new", "New"
    VERIFIED = "verified", "Verified"
    DONE = "done", "Done"
    PHOTO_DONE = "photo_done", "Photo Done"


class AuthType(models.TextChoices):
    VIA_EMAIL = "via_email", "VIA Email"
    VIA_PHONE = "via_phone", "VIA Phone"


class User(BaseModel, AbstractUser):
    auth_status = models.CharField(
        max_length=10, choices=AuthStatus.choices, default=AuthStatus.NEW
    )
    auth_type = models.CharField(
        max_length=10, choices=AuthStatus.choices, default=AuthType.VIA_EMAIL
    )
    email = models.CharField(max_length=128, null=True, unique=True)
    phone_number = models.CharField(max_length=128, null=True, unique=True)
    avatar = models.ImageField(upload_to="users/avatars/", null=True)

    # =============== CREATE CODE ===================
    def create_code(self, auth_type):
        code = "".join([str(randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(user=self, code=code, auth_type=auth_type)
        return code

    def check_username(self):
        if not self.username:
            temp_username = f"temp_username_{uuid.uuid4().__str__().split("-")[-1]}"
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{temp_username}{randint(1, 9)}"

            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower().strip()
            self.email = normalize_email

    def check_user_password(self):
        if not self.password:
            temp_password: str = (
                f"temp_password_{uuid.uuid4().__str__().split("-")[-1]}"
            )
            self.password = temp_password

    # ==================== CREATE TOKEN ====================
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def password_hashing(self):
        if not is_hashing(self.password):
            self.set_password(self.password)

    def clean(self):
        self.check_username()
        self.check_email()
        self.check_user_password()
        self.password_hashing()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.clean()
        else:
            self.check_email()

        if self.password and not is_hashing(self.password):
            self.set_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


EXPIRE_EMAIL = 2
EXPIRE_PHONE = 5


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify_code")
    expired_time = models.DateTimeField()
    auth_type = models.CharField(max_length=10, choices=AuthType.choices)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "code" , "is_confirmed")

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.auth_type == AuthType.VIA_EMAIL:
                self.expired_time = timezone.now() + timedelta(minutes=EXPIRE_EMAIL)
            elif self.auth_type == AuthType.VIA_PHONE:
                self.expired_time = timezone.now() + timedelta(minutes=EXPIRE_PHONE)

        super().save(*args, **kwargs)

    def is_expired(self):
        if self.expired_time is None:
            return True
        return timezone.now() > self.expired_time

    def can_confirmed(self):
        if self.is_confirmed:
            return False
        if self.is_expired:
            return False

        return True
