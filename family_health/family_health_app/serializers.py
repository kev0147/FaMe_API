from rest_framework import serializers
from .models import *

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], password=validated_data['password'])
        return user
    
    def validate_password(self, value: str) -> str:
        return make_password(value)
    

class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profil
        fields = ['user', 'name', 'firstname', 'phone_number', 'email']

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

class BalanceSerializer(serializers.ModelSerializer):
    #patient_balance = PatientSerializer
    class Meta:
        model = Balance
        fields = ['balance']

    def create(self):
        balance = Balance.objects.create(balance=7000)
        return balance
        

class PatientSerializer(serializers.ModelSerializer):
    profil = ProfilSerializer()
    balance = BalanceSerializer()
    class Meta:
        model = Patient
        fields = ['profil', 'birth_date', 'gender', 'balance']

    def create(self, validated_data):
        balance = validated_data.pop('balance')
        balance = Balance.objects.create(**balance)
        profil = validated_data.pop('profil')
        user = profil.pop('user')
        user['username'] = profil['phone_number']
        user['password'] = profil['phone_number']
        user = User.objects.create(**user)
        profil = Profil.objects.create(user = user , **profil)
        patient = Patient.objects.create(profil=profil, balance=balance , **validated_data)
        return patient     