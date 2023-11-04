from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import *
from .serializers import PatientInscriptionSerializer, PatientValidationSerializer, PatientSerializer, UserSerializer, PrestationSerializer, ServiceSerializer, ReportSerializer, ProfileSerializer


class PatientInscriptionViewset(ModelViewSet):
    serializer_class = PatientInscriptionSerializer
    queryset = Patient.objects.all()

class PatientValidationViewset(ModelViewSet):
    serializer_class = PatientValidationSerializer
    queryset = Patient.objects.all()

class PatientViewset(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PrestationViewset(ModelViewSet):
    serializer_class = PrestationSerializer
    queryset = Prestation.objects.all()

class ServiceViewset(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

class ReportViewset(ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()