from django.contrib import admin
from .models import Doctor, Patient
from django.contrib.auth.models import User

class DoctorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(id=request.user.doctor.id)
        if hasattr(request.user, 'patient'):
             return qs.filter(patients=request.user.patient)
        return qs.none()

    list_display = ['name', 'specialty']

class PatientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(doctor=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            return qs.filter(id=request.user.patient.id)
        return qs.none()

    list_display = ['name', 'age', 'doctor']

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
