from datetime import timedelta
from rest_framework_simplejwt.tokens import Token
from users.models import User, AuthType

class RegsitrationToken(Token):
    
    token_type = "registration", 
    lifetime = timedelta(minutes=15)
    
    @classmethod
    def for_user(cls, user:User):
        token = cls()
        token['user_id'] = str(user.id)
        token["token_typr"] = "registration"
        token['current_step'] = user.auth_status
        
        if user.auth_type == AuthType.VIA_EMAIL:
            token['auth_type'] = AuthType.VIA_EMAIL
        elif user.auth_type ==  AuthType.VIA_PHONE:
            token['auth_type'] = AuthType.VIA_PHONE
        
        return token
    
    @classmethod
    def get_user_from_token(cls , token_str:str):
        try:
            token = cls(token_str)
            
            user_id = token.get("user_id")
            
            user =  User.objects.filter(id = user_id)
            
            return user
        except Exception:
            return None
        
