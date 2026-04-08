# ================= MODELS =============
from users.models import User

# ================= Dango ===============
from django.shortcuts import render

# ================= REST FRAMEWORK =====
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# ================ SERIALIZERS =========
from .serializers import RegisterEmialorNumberSerializers


class RegisterEmialorNumberView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = RegisterEmialorNumberSerializers
    permission_classes = [AllowAny]


# Create your views here.
