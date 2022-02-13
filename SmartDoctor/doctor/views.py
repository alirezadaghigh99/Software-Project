from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, ListView

# Create your views here.
from doctor.forms import DoctorRegisterForm, DoctorLoginForm
from patient.models import UserModel, UserRole, Visit


class DoctorSignupPage(FormView):
    model = UserModel
    template_name = 'doctor/doctor_signup.html'
    form_class = DoctorRegisterForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.cleaned_data['role'] = UserRole.DOCTOR
        form.save()
        return super().form_valid(form)


def login_page(request):
    form = DoctorLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('doctor:visit-request-list'))
    return render(request, 'doctor/doctor_login.html', {'form': form})


class PublisherListView(ListView):
    model = Visit
    template_name = 'doctor/visit_request_list.html'
