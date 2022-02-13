from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import FormView, ListView

from doctor.forms import DoctorRegisterForm, DoctorLoginForm
from patient.models import UserModel, UserRole, Visit, VisitStatus


# Create your views here.


class DoctorSignupPage(FormView):
    model = UserModel
    template_name = 'doctor/doctor_signup.html'
    form_class = DoctorRegisterForm
    success_url = 'login'

    def form_valid(self, form):
        form.cleaned_data['role'] = UserRole.DOCTOR
        data = form.cleaned_data
        user = UserModel(username=data["username"], first_name=data["first_name"], last_name=data["last_name"],
                         role=data["role"])
        user.set_password(data["password"])
        user.save()
        return super().form_valid(form)


def login_page(request):
    form = DoctorLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('doctor:visit-request-list'))
    return render(request, 'doctor/doctor_login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('doctor:login'))


class PublisherListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'doctor/visit_request_list.html'


@login_required
def accept_reject_visit(request, visit_id, accept):
    visit = get_object_or_404(Visit, pk=visit_id)
    if accept:
        visit.status = VisitStatus.ACCEPT
    else:
        visit.status = VisitStatus.REJECT
    visit.save()
    return HttpResponseRedirect(reverse('doctor:visit-request-list'))
