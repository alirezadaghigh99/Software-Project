from django.views.generic import FormView

# Create your views here.
from doctor.forms import DoctorRegisterForm
from patient.models import UserModel, UserRole


class DoctorSignupPage(FormView):
    model = UserModel
    template_name = 'doctor/doctor_signup.html'
    form_class = DoctorRegisterForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.cleaned_data['role'] = UserRole.DOCTOR
        return super().form_valid(form)
