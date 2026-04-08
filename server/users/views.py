# ================= Dango ===============
from django.shortcuts import render

# ================= REST FRAMEWORK =====
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

# ================ SERIALIZERS =========
from .serializers import RegisterEmialorNumberSerializers


class RegisterEmialorNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self , request):
        serializer = RegisterEmialorNumberSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)

# Create your views here.
