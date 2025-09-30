from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class RegistrationDB(models.Model):
    Name=models.CharField(max_length=100,null=True,blank=True)
    Password=models.CharField(max_length=100,null=True,blank=True)
    Confirm_Password=models.CharField(max_length=100,null=True,blank=True)
    Email=models.CharField(max_length=100,null=True,blank=True)



#Contact model

class ContactDB(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobpostDB(models.Model):

    Company_Image= models.ImageField(upload_to="jobpost", blank=True,null=True)
    Job_Category = models.CharField(max_length=100,null=True, blank=True)
    Job_Title = models.CharField(max_length=100,null=True, blank=True)
    Company_Name = models.CharField(max_length=100,null=True, blank=True)
    Job_Location = models.CharField(max_length=100,null=True, blank=True)
    Job_Salary = models.CharField(max_length=100,null=True, blank=True)
    Job_Description = models.TextField(max_length=100,null=True, blank=True)
    Required_Skills = models.CharField(max_length=100,null=True, blank=True)
    Education = models.CharField(max_length=100,null=True, blank=True)
    Experience = models.IntegerField(null=True, blank=True)
    Job_type = models.CharField(max_length=100,null=True, blank=True)
    Vacancy = models.IntegerField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Job_Title


class JobApplicationDB(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
    ]

    job = models.ForeignKey(JobpostDB, on_delete=models.CASCADE, default=1)  # Default Job ID = 1
    # Personal Details
    full_name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=100,null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=150,null=True, blank=True)
    date_of_birth = models.DateField()

    # Education
    highest_qualification = models.CharField(max_length=100,null=True, blank=True)
    university = models.CharField(max_length=150,null=True, blank=True)
    passing_year = models.IntegerField(null=True, blank=True)

    # Work Experience
    experience_years = models.IntegerField(null=True, blank=True)
    previous_company = models.CharField(max_length=200, blank=True, null=True)
    previous_role = models.CharField(max_length=200, blank=True, null=True)

    # Resume Upload
    resume = models.FileField(upload_to="resumes/")

    applied_on = models.DateTimeField(default=now)  # Ensure this line is present
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Applied")  # Added Status Field

    def __str__(self):
        return f"{self.full_name} applied for {self.job.Job_Title}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User model
    profile_picture = models.ImageField(upload_to="profile_pictures/", default="default_profile.jpg", blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)  # For job seekers
    company_name = models.CharField(max_length=100, blank=True, null=True)  # For employers
    is_employer = models.BooleanField(default=False)  # Distinguish between employers and job seekers

    def __str__(self):
        return self.user.username


