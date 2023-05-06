from django.db import models
from django.db.models import UniqueConstraint
import uuid
class Doctor(models.Model):
    #doctor_id=models.UUIDField(primary_key=True,default=uuid.uuid4().int % 10000,editable=False,unique=True)
    doctor_id = models.IntegerField(primary_key=True, editable=False, unique=True)
    email_id=models.EmailField(max_length=50,unique=True)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    #nmc_id = models.IntegerField(help_text = "Enter your IMR registration number")
    #state=models.CharField(help_text="Which state's medical council?",max_length=15)
    #year=models.CharField(max_length=5)
    password = models.CharField(max_length=100,default="password")

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            # generate a UUID and convert it to an integer
            self.doctor_id =uuid.uuid4().int % 100000 
        super(Doctor, self).save(*args, **kwargs)
    
    class Meta:
        db_table='Doctor'
        
class Patient(models.Model):
    CHOICES =(
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),)
    patient_id=models.IntegerField(primary_key=True,editable=False, unique=True)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    Age=models.IntegerField()
    Gender=models.CharField(choices=CHOICES,max_length=10)
    UniqueConstraint(fields=['patient_id','doctor_id'],name='p_key')

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # generate a UUID and convert it to an integer
            self.patient_id =uuid.uuid4().int % 100000 
        super(Patient, self).save(*args, **kwargs)
    
    class Meta:
        db_table='patient'

class Report(models.Model):
    CHOICES =(
    ("Pneumonia", "Pneumonia"),
    ("Malaria", "Malaria"),
    ("Brain Cancer","Brain Cancer"))
    report_id=models.IntegerField(primary_key=True,editable=False, unique=True)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    Report_text=models.CharField(max_length=300)
    Image_URL=models.CharField(max_length=400,default='default')
    Report_URL=models.CharField(max_length=400)
    disease_name=models.CharField(choices=CHOICES,max_length=100)
    UniqueConstraint(fields=['patient_id','doctor_id','report_id'],name='p_key')

    def save(self, *args, **kwargs):
        if not self.report_id:
            # generate a UUID and convert it to an integer
            self.report_id =uuid.uuid4().int % 100000 
        super(Report, self).save(*args, **kwargs)

    class Meta:
        db_table="Report" 

 
    
