from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from patient.models import UserModel
from .forms import PatientRegisterForm
from . import views
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from ..patient.models import UserRole


def register(request):
    if request.method == 'POST':
        details = PatientRegisterForm(request.POST)
        if details.is_valid():
            user = details.save(commit=False)
            user.save()
            return redirect(reverse('patient_new:login'))

        else:

            return render(request, "signup.html", {'form': details})
    else:
        form = PatientRegisterForm(None)
        return render(request, 'signup.html', {'form': form})


def login(request):
    form = PatientRegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('patient:doctor-list'))
    return render(request, 'patient/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('patient:login'))

@login_required
def doctors_list(request):
    doctors = UserModel.objects.filter(role=UserRole.DOCTOR)
    return render(request, "patient/doctors-list.html", {"doctors":doctors})

@login_required
def make_appointment(request, doctor_id)



