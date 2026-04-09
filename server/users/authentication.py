from users.models import User
from .tokens import RegsitrationToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegistrationTokenAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token):
        try:
            return RegsitrationToken(raw_token)
        except Exception as e:
            raise AuthenticationFailed(f"Token yaroqsiz : {str(e)}")

    def get_user(self, validated_token):

        try:
            user_id = validated_token.get("user_id", None)

            if user_id is None:
                raise AuthenticationFailed("Token ichida user_id yoq")

            user: User = User.objects.get(id=user_id)
            
            if user.auth_status != validated_token.get("current_step"):
                raise AuthenticationFailed("Token yaroqsiz")
            
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed("user topilmadi")
        except Exception as e:
            raise AuthenticationFailed(f"Token Xatosi : {str(e)}")
