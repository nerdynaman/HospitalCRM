from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    doctors = models.ManyToManyField(Doctor, related_name="patients")

    def __str__(self):
        return f"{self.name}"

class LabTechnician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Test(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
class Accountant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.specialty})"
    
    

class Session(models.Model):
    name = models.CharField(max_length=100)
    doctor = models.ManyToManyField(Doctor, related_name="sessions")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField()
    totalPayment = models.IntegerField(null=True, blank=True)
    test = models.ManyToManyField(Test, related_name="sessions", blank=True)
    labTechnician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE, null=True, blank=True)
    # testResults = models.ManyToManyField(TestResult, through='TestResult', related_name="sessions", blank=True)

    def __str__(self):
        return f"Session - {self.name}"
    
class TestResult(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.TextField()
    labTechnician = models.ForeignKey(LabTechnician, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.session} - {self.test} ({self.date} {self.time})"
