from django.contrib import admin
from .models import Resume, Experience, Skill, Certification, Education
# Register your models here.

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Certification)
admin.site.register(Education)
