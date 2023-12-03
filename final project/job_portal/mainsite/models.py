from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        Employer = "EMPLOYER", "Employer"
        Applicant = "APPLICANT", "Applicant"
    role = models.CharField(max_length=50, choices=Role.choices)

class Address(models.Model):
    street = models.CharField(default="", max_length=200)
    city = models.CharField(default="", max_length=200)
    state = models.CharField(default="", max_length=2)
    zip = models.CharField(default="", max_length=5)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip}"


class Applicant(User):
    base_role = User.Role.Applicant
    class Meta:
        proxy = True

class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    birth_day = models.DateField(default=date(2000, 1, 1))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='applicant_addresses', null=True,
                                blank=True)
    profile_picture = models.ImageField(default='profile_images/profilepic.jpg', upload_to='profile_images/')
    phone = models.CharField(max_length=10, default="")
    linkedin_url = models.CharField(max_length=500, default="")
    resume = models.FileField(upload_to='documents/', blank=True, null=True)

class Employer(User):
    base_role = User.Role.Employer
    class Meta:
        proxy = True

class EmployerProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    name = models.CharField(default="", max_length=100)
    phone = models.CharField(default="", max_length=10)
    industry = models.CharField(default="", max_length=100)
    company_size = models.PositiveIntegerField(default=0)
    found_date = models.DateField(default=date(2000, 1, 1))
    company_url = models.CharField(default="", max_length=500)
    description = models.TextField(default="", max_length=2000)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='employer_addresses', null=True,
                                blank=True)
    #admin will check company account and email or phone verify if the account is valid, so they can post a job
    is_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=500)
    job_type = models.CharField(max_length=100) #parttime, fulltime, intern, ....
    location = models.CharField(max_length=100) #remote, hybrid, on-site
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='job_location')
    description = models.TextField(max_length=2000)
    job_url = models.CharField(max_length=1000)
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    applicants = models.ManyToManyField(ApplicantProfile, related_name='applied_jobs', null=True, blank = True)
    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.Applicant and not hasattr(instance, 'applicant_profile'):
            ApplicantProfile.objects.create(user=instance)
        elif instance.role == User.Role.Employer and not hasattr(instance, 'employer_profile'):
            EmployerProfile.objects.create(user=instance)
