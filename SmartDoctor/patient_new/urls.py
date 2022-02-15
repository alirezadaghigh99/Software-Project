from django.urls import path

# importing views from views..py
from .views import index, register, login_view, logout_view,doctors_list, make_appointment
app_name="patient_new"

urlpatterns = [
    path('signup/', register, name='signup'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('doctor-list', doctors_list, name='doctor-list'),
    path('make_appointment/<doctor_id>', make_appointment, name='make_appointment'),
    path('', index, name='index'),
]
