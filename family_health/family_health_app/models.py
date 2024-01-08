import django
from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.IntegerField()
    #phone_number = models.PhoneNumberField_("")

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, related_name='doctor', on_delete=models.CASCADE, blank=True)
    doctors_order_number = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50, default='generalist')
    validated = models.BooleanField(default=False)

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GENDERs = [
        ("F", "female"),
        ("M", "male"),
    ]
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERs)
    profile = models.OneToOneField(Profile, related_name='patient', on_delete=models.CASCADE, blank=True)
    validated = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, related_name='patients', on_delete=models.CASCADE, null=True)

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


class Administrator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Message(models.Model):
    date = models.DateField()
    file_path = models.CharField(max_length=100, null=True, default='')
    sender = models.ForeignKey(Profile, related_name= 'messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name= 'messages_received', on_delete=models.CASCADE)