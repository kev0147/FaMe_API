"""
URL configuration for family_health project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from family_health_app.views import GetPatientFromTokenViewset, MessagesViewset, NonValidatedDoctorViewset, NonValidatedPatientViewset, PatientInscriptionViewset, PatientValidationViewset, PatientViewset, ProfileViewset, ReportViewset, ServiceViewset, UserViewset, PrestationViewset, DoctorViewset, DoctorInscriptionViewset, DoctorValidationViewset, ProfileMessagesViewset

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





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

