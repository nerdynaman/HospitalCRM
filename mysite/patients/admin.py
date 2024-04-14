from django.contrib import admin
from .models import Doctor, Patient, LabTechnician, Test, Accountant, Session
from django import forms
from django.contrib.auth.models import User

class DoctorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(id=request.user.doctor.id)
        # if it is a patient, show all doctors
        elif hasattr(request.user, 'patient'):
             return qs
        return qs.none()

    list_display = ['name', 'specialty']

class PatientAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(doctors=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            return qs.filter(id=request.user.patient.id)
        return qs.none()

    list_display = ['name', 'age', 'display_doctors']

    def display_doctors(self, obj):
        return ", ".join([doctor.name for doctor in obj.doctors.all()])
    display_doctors.short_description = 'Doctors'

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)

# class SessionAdminForm(forms.ModelForm):
#     class Meta:
#         model = Session
#         fields = '__all__'  # Specify all fields that should be included initially

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#         user = self.request.user if self.request else None
#         if user and not user.is_superuser:
#             if hasattr(user, 'accountant'):
#                 # Restrict fields for accountants
#                 restricted_fields = ['doctor', 'patient', 'date', 'time', 'notes']
#                 self.fields.pop('test', None)  # Accountants should not edit test details
#                 for field_name in restricted_fields:
#                     if field_name in self.fields:
#                         self.fields.pop(field_name)
#             elif hasattr(user, 'labtechnician'):
#                 # Restrict fields for lab technicians
#                 restricted_fields = ['doctor', 'patient', 'date', 'time', 'notes', 'totalPayment']
#                 for field_name in restricted_fields:
#                     if field_name in self.fields:
#                         self.fields.pop(field_name)
            # elif hasattr(user, 'doctor'):
            #     # Restrict fields for doctors
            #     restricted_fields = ['totalPayment', 'patient']
            #     for field_name in restricted_fields:
            #         if field_name in self.fields:
            #             self.fields.pop(field_name)

class SessionAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(doctor=request.user.doctor)
        elif hasattr(request.user, 'labtechnician'):
            return qs.filter(test__labtechnician=request.user.labtechnician)
        elif hasattr(request.user, 'accountant'):
            return qs
        elif hasattr(request.user, 'patient'):
            return qs.filter(patient=request.user.patient)
        return qs.none()

    def display_doctors(self, obj):
        return ", ".join([doctor.name for doctor in obj.doctor.all()])
    display_doctors.short_description = 'Doctors'
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if hasattr(request.user, 'doctor'):
            for i in fields:
                 if i == 'totalPayment':
                      fields.remove(i)
        if hasattr(request.user, 'labtechnician'):
             for i in fields:
                  if i in ['doctor', 'patient', 'date', 'time', 'notes', 'totalPayment']:
                       fields.remove(i)
        if hasattr(request.user, 'accountant'):
             for i in fields:
                  if i in ['doctor', 'patient', 'date', 'time', 'notes']:
                       fields.remove(i)
        return fields
    
    def get_readonly_fields(self, request, obj=None):
        return ['patient']

    list_display = ['patient', 'display_doctors', 'date']

admin.site.register(Session, SessionAdmin)
admin.site.register(Test)
admin.site.register(LabTechnician)
admin.site.register(Accountant)