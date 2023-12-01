from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from patient_managment.serializers import PatientSerializer, PrestationSerializer, AppointmentSerializer, UserSerializer
from patient_managment.models import Prestation, Patient, Appointment, User
from patient_managment.permissions import IsAuthenticated


# Create your views here.

class MultipleSerializerMixin:
    detail_serializer_class = None
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    
class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.all()

class PatientViewset(ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Patient.objects.all()

class PrestationViewset(ModelViewSet):
    serializer_class = PrestationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Prestation.objects.all()
    
class AppointementViewset(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Appointment.objects.all()