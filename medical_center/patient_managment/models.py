import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Patient(models.Model):
    patient_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_name = models.CharField(max_length=50)
    patient_firstname = models.CharField(max_length=100)
    patient_contact = models.IntegerField()
    patient_email = models.EmailField()



class Prestation(models.Model):
    prestation_name = models.CharField(max_length=500)



class Appointment(models.Model):
    def deletedPatient():
        return Patient.objects.create(patient_lastname = 'deleted', patient_firstname='deleted')
    
    def deletedPrestation():
        return Prestation.objects.create(prestation_name='deleted')

    appointment_creation_date = models.DateTimeField(auto_now_add=True)
    appointment_date = models.DateTimeField()
    patient = models.ForeignKey(Patient, related_name='patient_appointments', default=[], on_delete=models.CASCADE)
    prestation = models.ForeignKey(Prestation, related_name='prestation_appointments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['appointment_creation_date']



class Information(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information_date = models.DateTimeField(auto_now_add=True)
    information_title = models.CharField(max_length=500)
    information = models.TextField()

    class Meta:
        ordering = ['information_date']

"""
class Health_book(models.Model):
    health_book_creation_date = models.DateTimeField(auto_now_add=True)
    patient = models.OneToOneField(Patient, primary_key=True)

class Health_book_event(models.Model):
    health_book_event = models.CharField()
    health_book_event_date = models.DateTimeField(auto_now_add=True)
    health_book_event_comments = code = models.TextField()
    Health_book = models.ForeignKey(Health_book)
"""
    
