from cgi import test
from math import e
from re import T
from django.contrib import admin
from .models import Doctor, Patient, LabTechnician, Test, Accountant, Session, TestResult
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

# # First, unregister the existing User admin
# admin.site.unregister(User)

# # Now, create a custom UserAdmin class
# class CustomUserAdmin(UserAdmin):
#     def has_view_permission(self, request, obj=None):
#         # This function is called to check if the history button should be visible
#         if request.path.endswith('history/'):
#             return False
#         return super().has_view_permission(request, obj)

#     def history_view(self, request, object_id, extra_context=None):
#         # This function renders the history page
#         # You can either raise a PermissionDenied error or simply not call the parent method
#         return HttpResponseRedirect('/admin/auth/user/')

# # Finally, register your custom UserAdmin
# admin.site.register(User, CustomUserAdmin)

class DoctorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        '''
        This method is used to filter the queryset based on the user's role.
        Any user will only be able to view doctors that are associated with them.
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(id=request.user.doctor.id)
        # if it is a patient, show all doctors
        elif hasattr(request.user, 'patient'):
             return qs.filter(patients=request.user.patient)
        return qs.none()

    def history_view(self, request, object_id, extra_context=None):
        # This function renders the history page
        # You can either raise a PermissionDenied error or simply not call the parent method
        # show http response that you dont have permission
        return HttpResponseRedirect('/admin/')

    list_display = ['name', 'specialty']

class PatientAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        '''
        This method is used to filter the fields that are displayed based on the user's role.
        Mainly we have removed the doctors field from the form for doctors, lab technicians and accountants.
        This is done to ensure that privacy of the patients is maintained and that only the patient can view their doctors.
        '''
        fields = super().get_fields(request, obj)
        if hasattr(request.user, 'patient'):
            return fields
        if hasattr(request.user, 'doctor'):
             for i in fields:
                  if i == 'doctors':
                         fields.remove(i)
        if hasattr(request.user, 'labtechnician'):
             for i in fields:
                  if i == 'doctors':
                       fields.remove(i)
        if hasattr(request.user, 'accountant'):
             for i in fields:
                  if i == 'doctors':
                       fields.remove(i)
                               
        return fields
    def get_queryset(self, request):
        '''
        This method is used to filter the queryset based on the user's role.
        Only admin account has access to view all patients as it primarily used for management purposes.
        Further only doctors can view patients that are associated with them.
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'doctor'):
            return qs.filter(doctors=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            return qs.filter(id=request.user.patient.id)
        return qs.none()
    
    def history_view(self, request, object_id, extra_context=None):
        # This function renders the history page
        # You can either raise a PermissionDenied error or simply not call the parent method
        # show http response that you dont have permission
        return HttpResponseRedirect('/admin/')
    list_display = ['name', 'age']

    # def display_doctors(self, obj):
    #     return ", ".join([doctor.name for doctor in obj.doctors.all()])
    # display_doctors.short_description = 'Doctors'

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)


class SessionAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        '''
        This method is used to filter the queryset based on the user's role.
        Any user will only be able to view sessions that are associated with them.
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.none()
        if hasattr(request.user, 'doctor'):
            return qs.filter(doctor=request.user.doctor)
        elif hasattr(request.user, 'labtechnician'):
            return qs.filter(labTechnician=request.user.labtechnician)
        elif hasattr(request.user, 'accountant'):
            return qs #modify this
        elif hasattr(request.user, 'patient'):
            return qs.filter(patient=request.user.patient)
        return qs.none()
    
    def get_fields(self, request, obj=None):
        '''
        Depending upon the user's role, the fields that are displayed are different to maintain privacy and security.
        '''
        fields = super().get_fields(request, obj)
        if hasattr(request.user, 'doctor'):
            for i in fields:
                 if i == 'totalPayment':
                      fields.remove(i)
        elif hasattr(request.user, 'labtechnician'):
             for i in fields:
                  if i in ['doctor', 'patient', 'date', 'time', 'notes', 'totalPayment']:
                       fields.remove(i)
        elif hasattr(request.user, 'accountant'):
             for i in fields:
                  if i in ['doctor', 'patient', 'date', 'time', 'notes']:
                       fields.remove(i)
        return fields
    
    def has_add_permission(self, request):
        '''
        Only doctors can add sessions.
        '''
        if hasattr(request.user, 'doctor'):
            return True
        return False
        
    def get_readonly_fields(self, request, obj=None):
        '''
        Patient field should only be modified by doctors when session is made other than that it should be read only.
        '''
        if hasattr(request.user, 'doctor'):
            return []
        return ['patient']
    
    def save_related(self, request, form, formsets, change):
        '''
        It ensures the doctor who is creating the session is associated with the session.
        '''
        # If the user is a doctor, ensure they are associated with the session
        super().save_related(request, form, formsets, change)
        if hasattr(request.user, 'doctor'):
            obj = form.instance
            obj.doctor.add(request.user.doctor)
            obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        This ensures whenever a doctor is creating a session, only patients that are associated with them are displayed.
        '''
        if db_field.name == "patient":
            # Filter the queryset for the patient field based on existing relations with doctors
            if hasattr(request.user, 'doctor'):
                kwargs["queryset"] = Patient.objects.filter(doctors=request.user.doctor)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
         #  remove changes to totalPayment : prevent doctors from changing totalPayment MITM
         if hasattr(request.user, 'doctor'):
              if 'totalPayment' in form.changed_data:
                   print('totalPayment changed')
                   form.changed_data.remove('totalPayment')
         super().save_model(request, obj, form, change)

    def history_view(self, request, object_id, extra_context=None):
        # This function renders the history page
        # You can either raise a PermissionDenied error or simply not call the parent method
        # show http response that you dont have permission
        return HttpResponseRedirect('/admin/')
    
    # list_display = ['patient', 'display_doctors', 'date']

admin.site.register(Session, SessionAdmin)
admin.site.register(Test)
admin.site.register(LabTechnician)
admin.site.register(Accountant)
        
class TestResultAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        '''
        This prevents users from viewing the lab technician field in the form.
        '''
        self.exclude = ('labTechnician',)
        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        '''
        This method shows the test results based on the user's role.
        That is test results are generated by lab technicians for sessions and users part of that session can view the test results.
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.none()
        elif hasattr(request.user, 'doctor'):
            return qs.filter(session__doctor=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            return qs.filter(session__patient=request.user.patient)
        elif hasattr(request.user, 'labtechnician'):
            return qs.filter(labTechnician=request.user.labtechnician)
        return qs.none()

    def has_add_permission(self, request):
        '''
        Only lab technicians can add test results.
        '''
        return hasattr(request.user, 'labtechnician')

    def has_change_permission(self, request, obj=None):
        '''
        Only lab technicians can update test results.
        '''
        return hasattr(request.user, 'labtechnician') if obj else False

    def has_delete_permission(self, request, obj=None):
        '''
        Once a test result is generated, it should not be deleted.
        '''
        return False  # Assuming lab technicians cannot delete results

    def save_model(self, request, obj, form, change):
        '''
        this ensures whenever a lab technician is creating a test result, lab technician is associated with the test result.
        '''
        if not obj.pk and hasattr(request.user, 'labtechnician'):
            obj.labTechnician = request.user.labtechnician
        super().save_model(request, obj, form, change)

    def history_view(self, request, object_id, extra_context=None):
        # This function renders the history page
        # You can either raise a PermissionDenied error or simply not call the parent method
        # show http response that you dont have permission
        return HttpResponseRedirect('/admin/')
    
    list_display = ['session', 'test', 'result', 'labTechnician']
    
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     # If the user is a doctor, ensure they are associated with the session
    #     if hasattr(request.user, 'labtechnician'):
    #         obj = form.instance
    #         obj.labTechnician = request.user.labtechnician
    #         obj.save()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        '''
        This ensures whenever a lab technician is creating a test result, only sessions that are associated with them are displayed.
        '''
        if hasattr(request.user, 'labtechnician'):
             if db_field.name == "session":
                 # Filter the queryset for the patient field based on existing relations with doctors
                 kwargs["queryset"] = Session.objects.filter(labTechnician=request.user.labtechnician)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TestResult, TestResultAdmin)