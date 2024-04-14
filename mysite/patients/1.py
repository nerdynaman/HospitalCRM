from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Doctor, Patient

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'user')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.user == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.user == request.user
        return False

admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'doctor')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'doctor'):
            return qs.filter(doctor=request.user.doctor)
        else:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.doctor.user == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.doctor.user == request.user
        return False

admin.site.register(Patient, PatientAdmin)

class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'doctor'):
            return qs.filter(doctor__user=request.user)
        elif hasattr(request.user, 'patient'):
            return qs.filter(patient__user=request.user)
        else:
            return qs.none()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
