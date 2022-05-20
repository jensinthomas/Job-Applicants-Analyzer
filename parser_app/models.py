from django.db import models
from django import forms
from django.forms import ClearableFileInput

# for deleting media files after record is deleted
from django.dispatch import receiver
from regex import T
import os.path


class job(models.Model):
    jobdescription = models.FileField(upload_to='desc/')
    jobid = models.CharField('jobid', max_length=100, primary_key=True)
    jobrole = models.CharField('jobrole', max_length=100)
    jobdate = models.DateField()
    jobexp = models.CharField('jobrole', max_length=100)
    joblocation = models.CharField('joblocation', max_length=100)
    p1 = models.CharField('p1', max_length=100)
    p2 = models.CharField('p2', max_length=100)

    # class Meta:
    # db_table:"parser_app_job"

  #   class Meta:
   #      db_table:"job"


class Resume(models.Model):
    resume = models.FileField('Upload Resumes', upload_to='resumes/')
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField(
        'Mobile Number',  max_length=255, null=True, blank=True)
    education = models.CharField(
        'Education', max_length=255, null=True, blank=True)
    skills = models.CharField('Skills', max_length=1000, null=True, blank=True)
    company_name = models.CharField(
        'Company Name', max_length=1000, null=True, blank=True)
    college_name = models.CharField(
        'College Name', max_length=1000, null=True, blank=True)
    designation = models.CharField(
        'Designation', max_length=1000, null=True, blank=True)
    experience = models.CharField(
        'Experience', max_length=1000, null=True, blank=True)
    uploaded_on = models.DateTimeField('Uploaded On', auto_now_add=True)
    total_experience = models.CharField(
        'Total Experience (in Years)', max_length=1000, null=True, blank=True)
    matchpercentage = models.CharField(
        'Match Percentage', max_length=1000, null=True, blank=True)
    res = models.TextField(null=True, blank=True)
    fullname = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    exp = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=False, blank=False)
    qo1 = models.CharField(max_length=100, null=False, blank=False)
    qo2 = models.CharField(max_length=100, null=False, blank=False)
    qo3 = models.CharField(max_length=100, null=False, blank=False)
    qo4 = models.CharField(max_length=100, null=False, blank=False)
    qn1 = models.CharField(max_length=100, null=False, blank=False)
    qn2 = models.CharField(max_length=100, null=False, blank=False)
    qn3 = models.CharField(max_length=100, null=False, blank=False)
    qn4 = models.CharField(max_length=100, null=False, blank=False)
    qc1 = models.CharField(max_length=100, null=False, blank=False)
    qc2 = models.CharField(max_length=100, null=False, blank=False)
    qc3 = models.CharField(max_length=100, null=False, blank=False)
    qc4 = models.CharField(max_length=100, null=False, blank=False)
    qa1 = models.CharField(max_length=100, null=False, blank=False)
    qa2 = models.CharField(max_length=100, null=False, blank=False)
    qa3 = models.CharField(max_length=100, null=False, blank=False)
    qa4 = models.CharField(max_length=100, null=False, blank=False)
    qe1 = models.CharField(max_length=100, null=False, blank=False)
    qe2 = models.CharField(max_length=100, null=False, blank=False)
    qe3 = models.CharField(max_length=100, null=False, blank=False)
    qe4 = models.CharField(max_length=100, null=False, blank=False)
    jobs = models.CharField(max_length=100, null=False, blank=False)
    p = models.CharField(max_length=100, null=True, blank=True)
    # jobid = models.ForeignKey(job, on_delete=models.CASCADE)
    matching = models.IntegerField(null=True, blank=True)
    short = models.IntegerField(null=True, blank=True)


class applicants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    username = models.CharField(
        'Username', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField(
        'Mobile Number',  max_length=255, null=True, blank=True)
    password = models.CharField(
        'Password', max_length=255, null=True, blank=True)
    cpassword = models.CharField(
        'Confirm Password', max_length=255, null=True, blank=True)


class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }
