from rest_framework import serializers
from .models import *

from datetime import date
from password_generator import PasswordGenerator
from django.contrib.auth.hashers import make_password
passwordGenerator = PasswordGenerator()

class ProfileNoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'firstname', 'phone_number', 'email', 'patient']

    def update(self, instance, validated_data):
        instance.user = validated_data.user
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileNoUserSerializer()
    class Meta:
        model = User
        fields = ['username', 'password', 'id', 'profile']
        #extra_kwargs = {'password': {'write_only': True}}
    
    def validate_password(self, value: str) -> str:
        return make_password(value)
    

class ProfilInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'firstname', 'phone_number', 'email']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['date', 'patient', 'prestation', 'report']

class PrestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestation
        fields = ['prestation', 'price']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['prescription', 'comments']
        

class PatientInscriptionSerializer(serializers.ModelSerializer):
    profile = ProfilInscriptionSerializer()
    class Meta:
        model = Patient
        fields = ['profile', 'birth_date', 'gender']

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        profile = Profile.objects.create(**profile)
        patient = Patient.objects.create(profile=profile, **validated_data)
        return patient     
    

class ProfilInscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user' ,'name', 'firstname', 'phone_number', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user' ,'name', 'firstname', 'phone_number', 'email']

class PatientSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Patient
        fields = ['id', 'profile', 'birth_date', 'gender', 'validated']

class ProfileNoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'firstname', 'phone_number', 'email']

    
class PatientValidationSerializer(serializers.ModelSerializer):
    profile = ProfileNoUserSerializer()
    class Meta:
        model = Patient
        fields = ['id', 'profile']

    def update(self, instance, validated_data):
        #user = User.objects.create(username = str(instance.profile.phone_number), password = make_password(passwordGenerator.shuffle_password(instance.profile.name+instance.profile.firstname+str(instance.profile.phone_number), 8)))
        user = User.objects.create(username = str(instance.profile.phone_number), password = make_password(str(instance.profile.phone_number)))
        user.save()
        profile = instance.profile
        profile.user = user
        profile.save()
        prestation = Prestation.objects.create(prestation='inscription', price = 7000)
        prestation.save()
        service = Service.objects.create(date=date.today(), patient=instance, prestation=prestation)
        service.save()
        instance.validated = True 
        instance.save()
        return instance