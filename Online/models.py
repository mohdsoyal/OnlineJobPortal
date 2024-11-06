from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=25 ,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=20 , null=True)
    type = models.CharField(max_length=15 , null=True)
    
    def __str__(self):
        return self.user.username
    
class Recruiter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=25 ,null=True)
    image = models.FileField(null=True)
    company = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    industry = models.CharField(max_length=234)
    type = models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=56)
    def __str__(self):
        return self.user.username   
    
class Jobs(models.Model):
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    job_title = models.CharField(max_length=255)
    job_salary = models.FloatField(max_length=25)
    image =    models.FileField()
    description = models.TextField()
    experience = models.CharField(max_length=50)
    location  = models.CharField(max_length=150)
    skill  = models.CharField(max_length=500)
    created_date  = models.DateField()
    
    def __str__(self):
        return self.job_title
    
    
class Apply(models.Model):
     job = models.ForeignKey(Jobs,on_delete=models.CASCADE)
     student = models.ForeignKey(StudentUser,on_delete=models.CASCADE)
     resume = models.FileField(null=True)
     applydate = models.DateField(null=True)
     def __str__(self):
        return str(self.student)
     
     
        
    
    
     
    
    

    
    