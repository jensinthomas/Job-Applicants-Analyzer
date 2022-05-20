from django.contrib import admin
from .models import Resume
from .models import job

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass
admin.site.register(job)