from django.urls import path

# importing views from views..py
from doctor.views import DoctorSignupPage, login_page, PublisherListView

urlpatterns = [
    path('signup', DoctorSignupPage.as_view()),
    path('login', login_page),
    path('visit-request-list', PublisherListView.as_view(), name='visit-request-list'),
]
