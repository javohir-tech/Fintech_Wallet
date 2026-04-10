from django.utils import timezone
from users.models import User , AuthStatus
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import InvalidToken , TokenError

class IsRegistrationToken(BasePermission):
    
    def has_permission(self, request, view):
        
        if not hasattr(request , "auth") or request.auth is None:
            return  False
        
        token_type = request.auth.get("token_type")
        
        return token_type == "registration"
    
class CanVerifyCodeSend(BasePermission):
    
    def  has_permission(self, request, view):
        
        if not hasattr(request, "auth") or request.auth is None:
            return False
        
        current_step = request.auth.get("current_step")
        
        return current_step ==  AuthStatus.NEW
    
class CanSetUsernamePasssword(BasePermission):
    
    def has_permission(self, request, view):
        
        if not hasattr(request , 'auth') or request.auth is None:
            return False
        
        current_step = request.auth.get("current_step")
        
        return current_step == AuthStatus.VERIFIED