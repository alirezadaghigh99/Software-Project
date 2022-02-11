from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    PATIENT = 'patient', 'Patient'
    DOCTOR = 'doctor', 'Doctor'


class Patient(AbstractUser):
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.PATIENT)

    @property
    def national_code(self):
        return self.username

    @property
    def name(self):
        return self.first_name
