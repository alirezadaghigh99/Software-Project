from rest_framework import serializers
from .models import Patient


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['username', 'password1', 'password2', 'first_name', 'role']

    def validated_password(self):
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        if password2 != password1:
            return serializers.ValidationError("passwords are not equal")

    def save(self, **kwargs):
        if Patient.objects.get(username = self.validated_data["username"]):
            return serializers.ValidationError("Duplicate Username")

        user = Patient(username=self.validated_data["username"], first_name=self.validated_data["first_name"], role=self.validated_data["role"])
        user.set_password(self.validated_data["password1"])
        user.save()
        return user

