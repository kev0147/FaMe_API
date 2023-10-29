from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import *
from .serializers import PatientSerializer


class PatientViewset(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    