from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminAuthenticated, IsPatientAuthenticated
from .models import *
from .serializers import MessageSerializer, PatientInscriptionSerializer, PatientToDoctorAttributionSerializer, PatientValidationSerializer, PatientSerializer, ProfileMessagesSerializer, UserSerializer, PrestationSerializer, ServiceSerializer, ReportSerializer, ProfileSerializer, DoctorInscriptionSerializer, DoctorValidationSerializer, DoctorSerializer
from rest_framework.decorators import action


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



class DoctorInscriptionViewset(ModelViewSet):
    serializer_class = DoctorInscriptionSerializer
    queryset = Doctor.objects.all()

class DoctorValidationViewset(ModelViewSet):
    serializer_class = DoctorValidationSerializer
    queryset = Doctor.objects.all()

class NonValidatedDoctorViewset(ModelViewSet):
    #permission_classes = [IsAdminAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.filter(validated=False)

class ValidatedDoctorViewset(ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.filter(validated=True)

class DoctorViewset(ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class MessagesViewset(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class ProfileMessagesViewset(ModelViewSet):
    serializer_class = ProfileMessagesSerializer
    queryset = Profile.objects.all()

class PatientToDoctorAttributionViewset(ModelViewSet):
    serializer_class = PatientToDoctorAttributionSerializer
    queryset = Patient.objects.all()



class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @action(methods=["put"], url_path=r'attribuer_docteur',detail=False)
    def attribuer_docteur(self, request, *args, **kwargs):
        id_doctor = self.request.query_params.get('id_doctor', None)
        id_patient = self.request.query_params.get('id_patient', None)
        if(id_doctor and id_patient):
            try:
                patient =Patient.objects.get(pk=id_patient)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient non trouvé.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                doctor =Doctor.objects.get(pk=id_doctor)
            except Doctor.DoesNotExist:
                return Response({'error': 'Docteur non trouvé.'}, status=status.HTTP_400_BAD_REQUEST)
            patient.doctor = doctor
            patient.save()
            return Response(PatientSerializer(patient).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Mauvaise requ......'}, status=status.HTTP_400_BAD_REQUEST)