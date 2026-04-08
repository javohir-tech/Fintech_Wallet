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


class RegisterEmialorNumberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterEmialorNumberSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "oxshadi",
            },
            status=status.HTTP_200_OK,
        )


# Create your views here.
