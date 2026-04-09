from django.urls import path
# ============== VIEWS ============
from .views import SingUpView , VerifyCodeView

urlpatterns = [
    path("singup/" , SingUpView.as_view()), 
    path("verify/" , VerifyCodeView.as_view())
]