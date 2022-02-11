from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


class SignUpPatient(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        signup_serializer = self.serializer_class(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        user = signup_serializer.save()
        return Response({"username": user.username},status=status.HTTP_201_CREATED)


class AuthorizeView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_200_OK)
        return Response(
            headers={
                'x-name': request.user.first_name,
                'x-national-code': request.user.username,
                'x-role': 'admin' if request.user.is_superuser else request.user.role,
            },
            status=status.HTTP_200_OK,
        )
