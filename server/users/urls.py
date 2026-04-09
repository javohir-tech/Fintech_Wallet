from django.urls import path

# ============== VIEWS ============
from .views import (
    SignUpView,
    VerifyCodeView,
    UpdateVerifyCode,
    UpdateUserView,
    UploadAvatarView,
    LogOutView,
    LoginView,
    ForgetPasswordView,
    UpdatePasswordView,
)

urlpatterns = [
    path("singup/", SignUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("update_verify/", UpdateVerifyCode.as_view()),
    path("update/", UpdateUserView.as_view()),
    path("avatar/", UploadAvatarView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("login/", LoginView.as_view()),
    path("forget/", ForgetPasswordView.as_view()),
    path("password/", UpdatePasswordView.as_view()),
]
