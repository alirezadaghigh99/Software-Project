from django.urls import path

# importing views from views..py
from doctor.views import DoctorSignupPage, login_page, PublisherListView, logout_view, accept_reject_visit

urlpatterns = [
    path('signup', DoctorSignupPage.as_view(), name='signup'),
    path('login', login_page, name='login'),
    path('logout', logout_view, name='logout'),
    path('visit-request-list', PublisherListView.as_view(), name='visit-request-list'),
    path('accept-reject-visit/<int:visit_id>/<int:accept>', accept_reject_visit, name='accept-reject-visit'),
]
