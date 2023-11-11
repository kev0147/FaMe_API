from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminAuthenticated, IsPatientAuthenticated
from .models import *
from .serializers import PatientInscriptionSerializer, PatientValidationSerializer, PatientSerializer, UserSerializer, PrestationSerializer, ServiceSerializer, ReportSerializer, ProfileSerializer


class PatientInscriptionViewset(ModelViewSet):
    serializer_class = PatientInscriptionSerializer
    queryset = Patient.objects.all()

class PatientValidationViewset(ModelViewSet):
    serializer_class = PatientValidationSerializer
    queryset = Patient.objects.all()

class NonValidatedPatientViewset(ModelViewSet):
    #permission_classes = [IsAdminAuthenticated]
    serializer_class = PatientSerializer
    queryset = Patient.objects.filter(validated=False)

class ValidatedPatientViewset(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.filter(validated=True)

class PatientViewset(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


#return a list of a single patient. the one who made the request
class GetPatientFromTokenViewset(ModelViewSet):
    #permission_classes = [IsPatientAuthenticated]
    #permission_classes = [IsAdminAuthenticated]
    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer 
    

    def list(self, request, *args, **kwargs):
        # Get the profile based on the current user
        profile = self.get_object()

        if profile:
            # If the profile exists, retrieve the corresponding patient
            patient = Patient.objects.filter(profile=profile).first()

            if patient:
                serializer = self.get_serializer(patient)
                return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_object(self):
        user = self.request.user
        try:
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return None


        
        

class PrestationViewset(ModelViewSet):
    serializer_class = PrestationSerializer
    queryset = Prestation.objects.all()

class ServiceViewset(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

class ReportViewset(ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
