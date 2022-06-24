from django.core.validators import RegexValidator
from django.db import models
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.

#HR Table
class HRD_table(models.Model):
   alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

   EID = models.CharField(max_length=7,primary_key=True,validators=[alphanumeric])
   Name = models.CharField(max_length=30,unique=True)
   DOJ = models.DateField()
   Designation = models.CharField(max_length=10)
   Department = models.CharField(max_length=10)
   Uan = models.IntegerField(unique=True)
   PF_accno = models.CharField(unique=True,max_length=15)
   ESIC = models.IntegerField(unique=True)
   Company_email = models.EmailField(unique=True)
   working_hrs =  models.FloatField()
   appraisal_due = models.DateField()
   salary = models.IntegerField()
   manager =  models.CharField(max_length=20)
   working_days = models.IntegerField()

   class Meta:
      db_table = "HR_table"

   def __str__(self):
	   return self.Name


      #Employee Table
class Employee(models.Model):
   alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
   Name = models.ForeignKey(HRD_table,on_delete=models.CASCADE)
   Email=models.CharField(max_length=50)
   aadhar=models.IntegerField()
   aadharDoc=models.FileField(upload_to='media/')
   Pan = models.CharField(max_length=10,validators=[alphanumeric])
   panDoc=models.FileField(upload_to='media/')
   passport=models.IntegerField()
   passportDoc=models.FileField(upload_to='media/')
   esicNum=models.IntegerField()
   esicDoc=models.ImageField(upload_to='media/')
   Address = models.CharField(max_length=100)
   PermanentAddress= models.CharField(max_length=100)
   Ph = models.IntegerField()
   Gender = models.CharField(max_length=10)
   DOB= models.DateField()
   #Email = models.CharField(max_length=30)
   Blood= models.CharField(max_length=10)
   EmergencyPh= models.IntegerField()
   Photo=models.ImageField(upload_to='media/')

   def save(self, *args, **kwargs):
        if not self.id:
            self.Photo = self.compressImage(self.Photo)
        super(Employee, self).save(*args, **kwargs)

   def compressImage(self,Photo):
        imageTemproary1 = Image.open(Photo)
        imageTemproary = imageTemproary1.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) )
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        Photo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % Photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return Photo


   class Meta:
      db_table = "Employee"

   def __str__(self):
      return self.Name.Name


#Family Details Table
class Family(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   name = models.CharField(max_length=30)
   age =models.IntegerField(default=0)
   relation = models.CharField(max_length= 10)
   occupation = models.CharField(max_length=20)
   contact = models.CharField(max_length=12)
   remarks = models.CharField(max_length=100,default=' ')
   class Meta:
      db_table = "Family"

   def __str__(self):
      return self.EID.Name


#Education Table
class Education(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   qualification = models.CharField(max_length=30)
   board = models.CharField(max_length=15)
   percentage = models.IntegerField()
   passing = models.IntegerField()

   class Meta:
      db_table = "Education"

   def __str__(self):
      return self.EID.Name


#Bank Table
class Bank(models.Model):
   alphanumeric = RegexValidator(
       r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   name = models.CharField(max_length=30)
   account = models.IntegerField()
   bank_name = models.CharField(max_length=50)
   branch = models.CharField(max_length=50)
   ifsc = models.IntegerField(validators=[alphanumeric])
   swift = models.CharField(max_length=30)
   iban = models.CharField(max_length=30)

   class Meta:
      db_table = "Bank"

   def __str__(self):
      return self.name

#Certification Table
class Certification(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   course = models.CharField(max_length=30)
   institution_name = models.CharField(max_length=30)
   board_name = models.CharField(max_length=30)
   Class = models.CharField(max_length=30)
   marks = models.PositiveIntegerField()

   class Meta:
      db_table = "Certification"

   def __str__(self):
      return self.EID.Name


#Employment History Table
class History(models.Model):
   EID = models.ForeignKey(HRD_table,on_delete=models.CASCADE)
   organization = models.CharField(max_length=50)
   designation = models.CharField(max_length=30)
   work = models.CharField(max_length=100)
   tools = models.CharField(max_length=50)
   last_salary = models.CharField(max_length=20)
   reason_of_leaving = models.CharField(max_length=100)

   class Meta:
         db_table = 'History'

   def __str__(self):
      return self.EID.Name


#Projects table
class Project(models.Model):
   PID = models.IntegerField()
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   Pname = models.CharField(max_length=50)
   customername = models.CharField(max_length=50,default="none")
   Department = models.CharField(max_length=50,default="none")
   StartDate = models.DateField(max_length=50)
   EndDate = models.DateField(max_length=50)
   location = models.CharField(max_length=50,default="none")
   ProjectDesc = models.CharField(max_length=100,default="none")

   class Meta:
      db_table = "Projects"

   def __str__(self):
      return self.Pname


#Task/Team table
class Team(models.Model):
   TaskName = models.CharField(max_length=30)
   Allocated = models.TimeField()
   ActualTime = models.TimeField()
   dates = models.DateField(null=True)

   class Meta:
      db_table = "Teams"

   def __str__(self):
      return self.TaskName


#Timesheet table
class Timesheet(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   Project = models.CharField(max_length=100)
   task = models.CharField(max_length=100)
   date = models.DateField(primary_key = True)
   Task_in_time = models.TimeField()
   Task_out_time = models.TimeField()
   approval = models.BooleanField(blank=True, default=False)

   class Meta:
      db_table = "TimeSheet"

   def __str__(self):
      return self.EID.Name

#Attendance table
class Attendance(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   in_time = models.TimeField()
   out_time = models.TimeField()
   date = models.DateField(auto_now=False, auto_now_add=False)

   class Meta:
      db_table = "Attendance"

   def __str__(self):
      return self.EID.Name



#leave table
class Leave(models.Model):
   EID = models.ForeignKey(HRD_table, on_delete=models.CASCADE)
   FromDate = models.DateField()
   ToDate = models.DateField()
   Reason=models.CharField(max_length=400)
   approvel=models.BooleanField(default=False)

   class Meta:
      db_table = "Leave"

   def __str__(self):
      return self.EID
