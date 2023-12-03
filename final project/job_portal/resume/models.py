from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="", null=True)
    last_name = models.CharField(max_length=100, default="", null=True)
    phone = models.CharField(max_length=20, default="", null=True)
    email = models.EmailField(max_length=30, default="", null=True)
    linkedIn = models.CharField(max_length=100, default="", null=True)
    summary = models.TextField(max_length=1000, blank=True)

class Experience(models.Model):
    resume = models.ForeignKey(Resume, related_name='experiences', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000)

class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='education', on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

class Certification(models.Model):
    resume = models.ForeignKey(Resume, related_name='certifications', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(max_length=200, blank=True)

