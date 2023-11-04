from django.db import models
import uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField()
    #phone_number = models.PhoneNumberField_("")

class Patient(models.Model):
    GENDERs = [
        ("F", "female"),
        ("M", "male"),
    ]
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERs)
    profile = models.OneToOneField(Profile, related_name='patient', on_delete=models.CASCADE, blank=True)
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
    report = models.OneToOneField(Report, on_delete=models.CASCADE, null=True)

class Agent(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)

class Administrator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)