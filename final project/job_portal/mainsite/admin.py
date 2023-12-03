from django.contrib import admin
from .models import Address, User, ApplicantProfile, EmployerProfile, Job

# Register Address
admin.site.register(Address)

admin.site.register(User)

admin.site.register(ApplicantProfile)

admin.site.register(EmployerProfile)

admin.site.register(Job)
