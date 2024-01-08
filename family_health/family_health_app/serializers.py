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
        fields = ['name', 'firstname', 'phone_number', 'email', 'patient', 'doctor']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileNoUserSerializer()
    class Meta:
        model = User
        fields = ['username', 'password', 'profile', 'user_permissions', 'groups']
    
    
class PatientUserInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        #extra_kwargs = {'password': {'write_only': True}}
    
class DoctorUserInscriptionSerializer(serializers.ModelSerializer):
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
        patient_permission = Permission.objects.get_or_create(codename='doctor_permission')
        user.user_permissions.add(patient_permission)
        group = Group.objects.get_or_create(name='doctor')
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
        fields = ['id', 'profile', 'birth_date', 'gender', 'validated', 'doctor']

class PatientIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id']

class ProfileNoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'firstname', 'phone_number', 'email']

class ProfileIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user' ,'name', 'firstname', 'phone_number', 'email']

    
#to validate a patient is to give him access to the services. To validate him: we make a put request with the id of the patient. retrieving this patient, we retrieve the profile object of that patient. create a user whose username and password will be the profile phone number. then w
class PatientValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = []

    def update(self, instance, validated_data):
        user_data = {
            'username': str(instance.profile.phone_number),
            'password': make_password(str(instance.profile.phone_number)) # For demo purposes,I have to improve password handling
        }
        user = User.objects.create(**user_data)
        user.groups.add(Group.objects.get(name='patient'))
        user.user_permissions.add(Permission.objects.get(codename='patient_permission'))
        profile=instance.profile
        profile.user = user
        profile.save()
        print(f"{profile} updated successfully")

        prestation = Prestation.objects.get(id=1)
        service = Service(date=date.today(), patient=instance, prestation=prestation)
        service.save()

        instance.validated = True
        instance.save()

        return instance

    


class DoctorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Doctor
        fields = ['id', 'profile', 'validated', 'doctors_order_number', 'patients']


class DoctorIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id']


class PatientUpdateDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = Patient
        fields = ['doctor']

    def update(self, instance, validated_data):
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.save()
        return instance

#######################################################################################################

class DoctorInscriptionSerializer(serializers.ModelSerializer):
    profile = ProfilInscriptionSerializer()
    class Meta:
        model = Doctor
        fields = ['profile', 'doctors_order_number']

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
        
        doctor = Doctor.objects.create(profile=profile_instance, validated=False, **validated_data)
        return doctor 
    

class DoctorValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = []

    def update(self, instance, validated_data):
        user_data = {
            'username': str(instance.profile.phone_number),
            'password': make_password(str(instance.profile.phone_number)) # For demo purposes,I have to improve password handling
        }
        user = User.objects.create(**user_data)
        user.groups.add(Group.objects.get(name='doctor'))
        user.user_permissions.add(Permission.objects.get(codename='doctor_permission'))
        profile=instance.profile
        profile.user = user
        profile.save()
        print(f"{profile} updated successfully")

        
        #prestation = Prestation.objects.get(id=1)
        #service = Service(date=date.today(), patient=instance, prestation=prestation)
        #service.save()
        

        instance.validated = True
        instance.save()

        return instance
    

########################################################################################################
class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    class Meta:
        model = Message
        fields = [ 'sender_id', 'receiver_id', 'file_path']

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        receiver_id = validated_data.pop('receiver_id')

        sender_profile = Profile.objects.get(id=sender_id)
        receiver_profile = Profile.objects.get(id=receiver_id)

        message = Message.objects.create(
            date=date.today(),
            sender=sender_profile,
            receiver=receiver_profile,
            file_path=validated_data.get('file_path')
        )

        return message
    
class ProfileMessagesSerializer(serializers.ModelSerializer):
    messages_sent = MessageSerializer(many=True)
    messages_received = MessageSerializer(many = True)
    class Meta:
        model = Profile
        fields = ['id','user' ,'name', 'firstname', 'phone_number', 'messages_sent', 'messages_received']


class PatientToDoctorAttributionSerializer(serializers.ModelSerializer):
    doctor = DoctorIdSerializer()
    class Meta:
        model = Patient
        fields = '__all__'

    def update(self, instance, validated_data):
        doctor_data = validated_data.pop('doctor', None)

        # Update patient fields
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.validated = validated_data.get('validated', instance.validated)
        instance.save()

        if doctor_data:
            # If doctor data is provided, update the associated doctor
            doctor_instance = instance.doctor
            if doctor_instance:
                # If patient already has a doctor, update the doctor fields
                doctor_serializer = DoctorSerializer(doctor_instance, data=doctor_data)
            else:
                # If patient does not have a doctor, create a new doctor
                doctor_serializer = DoctorSerializer(data=doctor_data)

            if doctor_serializer.is_valid():
                doctor = doctor_serializer.save()
                instance.doctor = doctor

        return instance
    
class doctorAttributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = []

    def update(self, instance, validated_data):
        patient = PatientIdSerializer(data=validated_data)
        patient.is_valid()
        patient.save()
        patients = instance.patients
        patients.add(patient)
        instance.save()
        return instance

