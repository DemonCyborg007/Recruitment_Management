from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_facilitator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # Add this line
# Manually Set is_admin for Superuser
# When you create the superuser, manually set the is_admin flag:

# Create Superuser:

# bash code:
# python manage.py createsuperuser

# Manually set is_admin flag for the superuser:
# Open the Django shell:
# bash code:
# python manage.py shell

# Run the following commands:
# python code:
# from rec.models import User
# user = User.objects.get(username='your_superuser_username')
# user.is_admin = True
# user.save()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    enrollment = models.CharField(max_length=20, unique=True)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    tenth_grade = models.FloatField(null=True, blank=True)
    twelfth_grade = models.FloatField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

class Facilitator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

class PlacementDrive(models.Model):
    company_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    eligibility_criteria = models.TextField()
    date = models.DateField()
    facilitator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drives')

### Not tested from here
class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} applied to {self.drive.company_name}"
