# ===================== PYTHON =================
import uuid
from random import randint
from datetime import timedelta

# ===================== DJANGO =================
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import identify_hasher
from django.utils import timezone

# =================== SHARED ====================
from shared.models import BaseModel

# =================== REST FRAMEWORK ============
from rest_framework_simplejwt.tokens import RefreshToken


class AuthStatus(models.TextChoices):
    NEW = "new", "NEW"
    CODE_VERIFED = "code_verified", "Code veriftied"
    DONE = "done", "Done"
    PHOTO_DONE = "photo_done", "Photo Done"


class AuthType(models.TextChoices):
    VIA_EMAIL = "via_email", "Via Email"
    VIA_Phone = "via_phone", "Via Phone"


def is_hashed(password):
    try:
        identify_hasher(password)
        return True
    except Exception:
        return False


class User(BaseModel, AbstractUser):
    auth_status = models.CharField(
        max_length=13, choices=AuthStatus.choices, default=AuthStatus.NEW
    )
    auth_type = models.CharField(max_length=13, choices=AuthStatus.choices)
    photo = models.ImageField(upload_to="user/profile", blank=True, null=True)
    email = models.EmailField(max_length=128, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True, unique=True)

    # ///////////// CREATE  VERIFY CODE //////////////////
    def create_verify_code(self, auth_type):
        code = "".join([str(randint(0, 9)) for _ in range(4)])
        UserConfirmation.objects.create(user=self, code=code, auth_type=auth_type)
        return code

    def __str__(self):
        return self.username

    def check_username(self):
        if not self.username:
            temp_username = f"wallet-{uuid.uuid4().__str__().split("-")[-1]}"

            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{temp_username}{randint(1, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normilze_email = self.email.lower().strip()
            self.email = normilze_email

    def check_user_password(self):
        if not self.password:
            temp_username = f"wallet-{uuid.uuid4().__str__().split("-")[-1]}"
            self.password = temp_username

    def hashing_password(self):
        if not is_hashed(self.password):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def clean(self):
        self.check_username()
        self.check_user_password()
        self.hashing_password()
        self.check_email()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.clean()
        else:
            self.email()

        if self.password and not is_hashed(self.password):
            self.set_password(self.password)

        super().save(*args, *kwargs)


EXPIRE_EMAIL = 2
EXPIRE_PHONE = 5


class UserConfirmation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify_code")
    code = models.CharField(max_length=4)
    auth_type = models.CharField(max_length=9, choices=AuthType.choices)
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.auth_type == AuthType.VIA_Phone:
                self.expiration_date = timezone.now() + timedelta(minutes=EXPIRE_PHONE)
            elif self.auth_type == AuthType.VIA_EMAIL:
                self.expiration_date = timezone.now() + timedelta(minutes=EXPIRE_EMAIL)

        super().save(*args, **kwargs)

    def is_expired(self) -> bool:
        if self.expiration_date is None:
            return True
        return timezone.now() > self.expiration_date

    def can_verify(self) -> bool:
        if self.is_confirmed:
            return False
        if self.is_expired():
            return False

        return True
