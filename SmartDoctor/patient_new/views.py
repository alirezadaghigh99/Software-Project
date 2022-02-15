from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from patient.models import UserModel, Visit, VisitStatus
from .forms import PatientRegisterForm, PatientLoginForm
from . import views
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from patient.models import UserRole
def index(request):
    return render(request, 'patient_base.html', {})

def register(request):
    if request.method == 'POST':
        details = PatientRegisterForm(request.POST)
        if details.is_valid():
            user = details.save(commit=False)
            user.set_password(request.POST['password1'])
            user.save()
            return redirect(reverse('patient_new:login'))

        else:

            return render(request, "patient/signup.html", {'form': details})
    else:
        form = PatientRegisterForm(None)
        return render(request, 'patient/signup.html', {'form': form})


def login_view(request):
    form = PatientLoginForm(request.POST or None)
    if form.is_valid():

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('patient_new:doctor-list'))
    print(form.errors)
    return render(request, 'patient/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('patient_new:login'))


@login_required
def doctors_list(request):
    doctors = UserModel.objects.filter(role=UserRole.DOCTOR)
    return render(request, "patient/doctors-list.html", {"doctors": doctors})


@login_required
def make_appointment(request, doctor_id):
    if request.method == "POST":
        time = request.POST.get("time", "")
        time = str(time)
        doctor = UserModel.objects.get(id=doctor_id)
        patient = request.user
        visit = Visit(
            patient=patient,
            doctor=doctor,
            time=time,
            status=VisitStatus.PENDING
        )
        visit.save()
        return redirect(reverse('patient_new:doctor-list'))
