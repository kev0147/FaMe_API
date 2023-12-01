from datetime import timezone
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from patient_managment.models import Patient, Prestation, Appointment, User, Information


class PatientSerializer(serializers.ModelSerializer):
    patient_appointments = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = ['patient_id','patient_name', 'patient_firstname', 'patient_contact', 'patient_appointments']


class PrestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestation
        fields = ['id','prestation_name','prestation_appointments']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = ['appointment_creation_date', 'appointment_date', 'patient', 'prestation' ]
    
    def create(self, validated_data):
        patient = validated_data.pop('patient')
        patient = Patient.objects.create(**patient)
        validated_data['patient'] = patient
        return Appointment.objects.create(**validated_data)
    
    def validate_appointment_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate_password(self, value: str) -> str:
        return make_password(value)
