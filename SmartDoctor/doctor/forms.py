from django import forms

from patient.models import UserModel


class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'password', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
