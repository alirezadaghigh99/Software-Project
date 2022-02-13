from django.urls import path

# importing views from views..py
from doctor.views import DoctorSignupPage

urlpatterns = [
    path('signup', DoctorSignupPage.as_view()),
]
