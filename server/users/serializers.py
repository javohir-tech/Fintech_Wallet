from rest_framework import serializers

# ================= MODELS ================
from users.models import User, AuthType

# ================ SHARED ================
from shared.utility import check_user_input, send_email

# =============== DJANGO =================
from django.contrib.auth import authenticate


class RegisterEmialorNumberSerializers(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email_or_number"] = serializers.CharField(
            max_length=31, write_only=True
        )

    class Meta:
        model = User
        fields = ("id", "auth_type", "auth_status")
        extra_kwargs = {
            "id": {"read_only": True},
            "auth_type": {"read_only": True},
            "auth_status": {"read_only": True},
        }

    def validate(self, data):
        super().validate(data)
        data = self.auth_validate(data)
        data = self.is_exist(data)

        return data

    @staticmethod
    def auth_validate(data):
        user_input = data["email_or_number"]
        auth_type = check_user_input(user_input)
        if auth_type == AuthType.VIA_EMAIL:
            data = {"auth_type": AuthType.VIA_EMAIL, "email": user_input}
        elif auth_type == AuthType.VIA_PHONE:
            data = {"auth_type": AuthType.VIA_PHONE, "phone_number": user_input}
        else:
            raise serializers.ValidationError("email or phone_number is Invalid")

        return data

    @staticmethod
    def is_exist(data):
        auth_type = data["auth_type"]

        if auth_type == AuthType.VIA_EMAIL:
            email = data["email"]
            user = User.objects.filter(email=email).first()
            if user is not None:
                raise serializers.ValidationError("this email already exist")
        elif auth_type == AuthType.VIA_PHONE:
            phone = data["phone_number"]
            user = User.objects.filter(phone_number=phone).first()
            if user is not None:
                raise serializers.ValidationError("This phone number already exist")

        return data

    def create(self, validated_data):
        user = User(**validated_data)

        user.save()
        auth_type = validated_data["auth_type"]
        code = user.create_code(auth_type)
        if auth_type == AuthType.VIA_EMAIL:
            send_email(user.email, code)
        elif auth_type == AuthType.VIA_PHONE:
            send_email(user.phone_number, code)
            
        return user
