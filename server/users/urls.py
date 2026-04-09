from django.urls import path

# ============== VIEWS ============
from .views import (
    SingUpView,
    VerifyCodeView,
    UpdateVerifyCode,
    UpdateUserView,
    UploadAvatarView,
    LogOutView,
    LoginView
)

urlpatterns = [
    path("singup/", SingUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("update_verify/", UpdateVerifyCode.as_view()),
    path("update/", UpdateUserView.as_view()),
    path("avatar/", UploadAvatarView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("login/" , LoginView.as_view())
]
