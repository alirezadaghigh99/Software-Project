from rest_framework import serializers
from .models import Patient


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ['username', 'password1', 'password2', 'first_name', 'role']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password2 != password1:
            raise serializers.ValidationError("passwords are not equal")

    def save(self, **kwargs):

        try:
            patient = Patient.objects.get(username=self.validated_data["username"])
            raise serializers.ValidationError("Duplicate Username")
        except Patient.DoesNotExist:

            user = Patient(username=self.validated_data["username"], first_name=self.validated_data["first_name"],
                           role=self.validated_data["role"])
            user.set_password(self.validated_data["password1"])
            user.save()
            return user
