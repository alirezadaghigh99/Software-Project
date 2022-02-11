from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SignUpPatient(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        signup_serializer = self.serializer_class(data=request.data)
        signup_serializer.is_valid(raise_exception=True)
        user = signup_serializer.save()
        return Response({"username": user.username}, status=status.HTTP_201_CREATED)


class AddVisitView(APIView):
    serializer_class = VisitSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        visit_serializer = self.serializer_class(data=request.data)
        visit_serializer.is_valid(raise_exception=True)
        visit = visit_serializer.save()
        return Response({"time": visit.time}, status=status.HTTP_201_CREATED)


class AuthorizeView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(
            headers={
                'x-name': request.user.first_name,
                'x-national-code': request.user.username,
                'x-role': 'admin' if request.user.is_superuser else request.user.role,
            },
            status=status.HTTP_200_OK,
        )


class ListDoctorAPIView(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = UserModel.objects.filter(role=UserRole.DOCTOR)
