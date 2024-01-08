from django.urls import path, include
from rest_framework import routers
from .views import GetPatientFromTokenViewset, MessagesViewset, NonValidatedDoctorViewset, NonValidatedPatientViewset, PatientInscriptionViewset, PatientToDoctorAttributionViewset, PatientValidationViewset, PatientViewSet, PatientViewset, ProfileViewset, ReportViewset, ServiceViewset, UserViewset, PrestationViewset, DoctorViewset, DoctorInscriptionViewset, DoctorValidationViewset, ProfileMessagesViewset

router = routers.SimpleRouter()
router.register('patient', PatientViewset, basename='patient')
router.register('patientInscription', PatientInscriptionViewset, basename='patientInscription')
router.register('patientValidation', PatientValidationViewset, basename='patientValidation')
router.register('profile', ProfileViewset, basename='profile')
router.register('user', UserViewset, basename='user')
router.register('prestation', PrestationViewset, basename='prestation')
router.register('service', ServiceViewset, basename='service')
router.register('report', ReportViewset, basename='report')
router.register('nonValidatedpatients', NonValidatedPatientViewset, basename='nonValidatedpatients')
router.register('getPatientFromToken', GetPatientFromTokenViewset, basename='getPatientFromToken')

router.register('doctor', DoctorViewset, basename='doctor')
router.register('doctorInscription', DoctorInscriptionViewset, basename='doctorInscription')
router.register('doctorValidation', DoctorValidationViewset, basename='doctorValidation')
router.register('nonValidateddoctors', NonValidatedDoctorViewset, basename='nonValidateddoctors')

router.register('messages', MessagesViewset, basename='messages')
router.register('profileMessages', ProfileMessagesViewset, basename= 'profileMessages')
router.register('patientToDoctorAttribution', PatientViewSet, basename= 'patientToDoctorAttribution')





urlpatterns = [
    path('api/', include(router.urls))
]