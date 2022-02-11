from rest_framework import serializers
from rest_framework.generics import ListAPIView

from .models import UserModel, Visit


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2', 'first_name', 'role']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password2 != password1:
            raise serializers.ValidationError("passwords are not equal")
        return attrs

    def save(self, **kwargs):

        try:
            patient = UserModel.objects.get(username=self.validated_data["username"])
            raise serializers.ValidationError("Duplicate Username")
        except UserModel.DoesNotExist:

            user = UserModel(username=self.validated_data["username"], first_name=self.validated_data["first_name"],
                             role=self.validated_data["role"])
            user.set_password(self.validated_data["password1"])
            user.save()
            return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name', 'id', 'username', 'role']


class VisitSerializer(serializers.ModelSerializer):
    doctor_name = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(),source='doctor', write_only=True)
    patient_name = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(),source='patient', write_only=True)

    class Meta:
        model = Visit
        fields = ['doctor_name', 'patient_name', 'time']

    def validate(self, attrs):
        doctor= attrs.get('doctor')
        patient= attrs.get('patient')
        if doctor.role != 'doctor':
            raise serializers.ValidationError('the user is not doctor')
        if patient.role != 'patient':
            raise serializers.ValidationError('the user is not patient')
        return attrs

    def save(self, **kwargs):
        doctor = self.validated_data['doctor']
        patient = self.validated_data['patient']
        time = self.validated_data['time']
        visit = Visit(time=time, doctor=doctor, patient=patient)
        visit.save()
        return visit
