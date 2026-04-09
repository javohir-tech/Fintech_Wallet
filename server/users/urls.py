from django.urls import path
# ============== VIEWS ============
from .views import SingUpView , VerifyCodeView , UpdateVerifyCode , UpdateUserView

urlpatterns = [
    path("singup/" , SingUpView.as_view()), 
    path("verify/" , VerifyCodeView.as_view()), 
    path("update_verify/" , UpdateVerifyCode.as_view()), 
    path("update/" , UpdateUserView.as_view())
]