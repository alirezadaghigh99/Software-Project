from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class SignUpPatient(APIView):
    serializer_class = UserSignUpSerializer

    def create(self, request):
        signup_serializer = self.serializer_class(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        user = signup_serializer.save()
        return Response(status=status.HTTP_201_CREATED)
