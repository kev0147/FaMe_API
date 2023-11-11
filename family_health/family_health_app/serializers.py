from rest_framework import serializers
from .models import *

from datetime import date
from password_generator import PasswordGenerator
from django.contrib.auth.hashers import make_password
passwordGenerator = PasswordGenerator()
from django.contrib.auth.models import Permission, Group

class ProfileNoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'firstname', 'phone_number', 'email', 'patient']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileNoUserSerializer()
    class Meta:
        model = User
        fields = ['username', 'password', 'profile', 'user_permissions', 'groups']
    
    
class UserInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        #extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        patient_permission = Permission.objects.get(codename='patient_permission')
        user.user_permissions.add(patient_permission)
        group = Group.objects.get(name='patient')
        user.groups.add(group)
        
        return user

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
        

#serializer to create a patient. but he is not validated yet. so the validated field is false by default. to do this, we take a profile object: name, firstname, email and phone number. we also take his gender and birth date that are part of the patient object. then we create a profile and affect this profil to the patient we registered
class PatientInscriptionSerializer(serializers.ModelSerializer):
    profile = ProfilInscriptionSerializer()
    class Meta:
        model = Patient
        fields = ['profile', 'birth_date', 'gender']

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        serializer = ProfilInscriptionSerializer(data=profile)
        if serializer.is_valid():
            profile_instance = serializer.save()
            print(f"{profile_instance} created successfully")
            # instance contains the newly created object
        else:
            # Handle serializer errors
            print(serializer.errors)
        
        patient = Patient.objects.create(profile=profile_instance, validated=False, **validated_data)
        return patient 
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id','user' ,'name', 'firstname', 'phone_number', 'email']

class PatientSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Patient
        fields = ['id', 'profile', 'birth_date', 'gender', 'validated']

class ProfileNoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'firstname', 'phone_number', 'email']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user' ,'name', 'firstname', 'phone_number', 'email']

    
#to validate a patient is to give him access to the services. To validate him: we make a put request with the id of the patient. retrieving this patient, we retrieve the profile object of that patient. create a user whose username and password will be the profile phone number. then w
class PatientValidationSerializer(serializers.ModelSerializer):
    profile = ProfileNoUserSerializer()
    class Meta:
        model = Patient
        fields = ['profile']

    def update(self, instance, validated_data):
        user_data = {
            'username': str(instance.profile.phone_number),
            'password': str(instance.profile.phone_number)  # For demo purposes,I have to improve password handling
        }
        print(instance.profile)
        user_serializer = UserInscriptionSerializer(data=user_data)
        profile=instance.profile
        if user_serializer.is_valid():
            user = user_serializer.save()
            print(f"{user} created successfully")
            profile.user = user
            profile.save()
            print(f"{profile} updated successfully")

            prestation = Prestation.objects.get(id=1)
            service = Service(date=date.today(), patient=instance, prestation=prestation)
            service.save()

            instance.validated = True
            instance.save()
        else:
            print(user_serializer.errors)

        return instance
    
