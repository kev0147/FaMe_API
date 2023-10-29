from django.db import models
import uuid
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone_number = models.IntegerField()
    #phone_number = models.PhoneNumberField_("")

class Balance(models.Model):
    balance = models.IntegerField()

class Patient(models.Model):
    GENDERs = [
        ("F", "female"),
        ("M", "male"),
    ]
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERs)
    balance = models.OneToOneField(Balance, related_name='patient_balance', on_delete=models.CASCADE, blank=True)
    profil = models.OneToOneField(Profil, related_name='profil', on_delete=models.CASCADE, blank=True)
    validated = models.BooleanField(default=False)

class Prestation(models.Model):
    prestation = models.CharField(max_length=50)
    price = models.IntegerField()

class Report(models.Model):
    prescription = models.CharField(max_length=50)
    comments = models.IntegerField()

class Service(models.Model):
    date = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE)
    report = models.OneToOneField(Report, on_delete=models.CASCADE)

class Agent(models.Model):
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)

class Administrator(models.Model):
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE)