from django import forms

from patient.models import UserModel


class PatientRegisterForm(forms.ModelForm):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'password2': forms.PasswordInput(),
            'password1': forms.PasswordInput(),
        }

    def clean(self):
        super(PatientRegisterForm, self).clean()
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            self._errors['password'] = "unmatch password"
        try:
            user = UserModel.objects.get(username=username)
            self._errors['username'] = "duplicate username"
        except:
            pass
        return self.cleaned_data


class PatientLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
