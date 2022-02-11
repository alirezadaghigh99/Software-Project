from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('signup/', SignUpPatient.as_view(), name='signup'),
    path('signin/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
    path('doctor-list/', ListDoctorAPIView.as_view(), name='doctor'),
    path('create_visit/', AddVisitView.as_view(), name='visit'),

]
