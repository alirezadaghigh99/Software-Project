from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    PATIENT = 'patient', 'Patient'
    DOCTOR = 'doctor', 'Doctor'


class UserModel(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.PATIENT)

    @property
    def national_code(self):
        return self.username

    @property
    def name(self):
        return self.first_name


class VisitStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPT = 'accept', 'Accept'
    REJECT = 'reject', 'Reject'


class Visit(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='doctor_visit')
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='patient_visit')
    status = models.CharField(max_length=10, choices=VisitStatus.choices, default=VisitStatus.PENDING)
    time = models.CharField(max_length=60)

    @property
    def status(self):
        return self.status
