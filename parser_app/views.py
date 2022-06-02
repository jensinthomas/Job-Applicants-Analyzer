from matplotlib.style import context
from resume_parser.settings import BASE_DIR
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm, job, applicants
from .forms import DocumentForm
from parser_app.models import job
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from .models import *
import pandas as pd
from numpy import *
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, Http404
import os.path
import shutil
from sys import argv
import docx2txt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class train_model:

    def train(self, qoi, qni, qci, qai, qei, age, gender):
        data = pd.read_csv('resume_parser/train dataset.csv')
        array = data.values
        drop_columns = ['Personality (Class label)']
        X = data.drop(drop_columns, axis=1)
        print(X)

        if gender == 'Male':
            X['Gender'] = 1
        else:
            X['Gender'] = 0

        y = data['Personality (Class label)']
        print(y)

        X['openness'].values
        X['conscientiousness'].values
        X['extraversion'].values
        X['agreeableness'].values
        X['neuroticism'].values

        if gender == "Male":
            a = 1
        else:
            a = 0

        mul_lr = linear_model.LogisticRegression(
            multi_class='multinomial', solver='newton-cg', max_iter=1000)
        np.where(X.values >= np.finfo(np.float32).max)
        X = X.fillna(X.mean())
        mul_lr.fit(X, y)
        X_train = X
        y_train = y
        print(X_train.shape, y_train.size)
        dt2 = DecisionTreeClassifier(criterion='entropy')
        dt2.fit(X_train, y_train)
        X_train
        testdata = pd.read_csv('resume_parser/test dataset.csv')
        print(testdata.columns)
        drop_columns = ['Personality (class label)']
        X_test = testdata.drop(drop_columns, axis=1)
        equiv = {"Male": 1, 'Female': 0}
        X_test['Gender'] = X_test['Gender'].map(equiv)
        y_test = testdata['Personality (class label)']
        y_pred = mul_lr.predict(X_test)
        y_pred
        y_pred_dt = dt2.predict(X_test)
        y_pred_dt
        dt_score = dt2.score(X_test, y_test)
        print(f"Decision Tree Classifier Accuracy score is {dt_score}")
        print(dt_score)
        dot_data = export_graphviz(dt2, out_file=None)
        print(dot_data)

        test = pd.DataFrame({'Gender': a, 'Age': age, 'openness': qoi, 'neuroticism': qni,
                             'conscientiousness': qci, 'agreeableness': qai, 'extraversion': qei}, index=[0])
        print(mul_lr.predict(test))

        return mul_lr.predict(test)

    def test(self, test_data):
        try:
            test_predict = list()
            for i in test_data:
                test_predict.append(int(i))
            y_pred = self.mul_lr.predict(int([test_predict]))
            return y_pred
        except:
            print("All Factors For Finding Personality Not Entered!")


def prediction_result(aplcnt_name, personality_values):
    "after applying a job"
    applicant_data = {"Candidate Name": aplcnt_name,
                      }

    age = personality_values[1]

    print("\n Candidate Entered Data \n")
    print(personality_values)

    personality = train_model()
    personality.test(personality_values)
    personality = train_model.test(personality_values)
    print("\n Predicted Personality \n")
    print(personality)
    return personality


def new(request, id):

    jb = job.objects.filter(jobid=id).first()
    print(id)
    file_form = UploadResumeModelForm(request.POST, request.FILES)
    files = request.FILES.getlist('resume')
    resumes_data = []
    if file_form.is_valid():
        for file in files:
            # saving the file
            resume = Resume(resume=file)
            resume.jobs = request.POST['jobs']
            resume.save()

            # extracting resume entities
            parser = ResumeParser(os.path.join(
                settings.MEDIA_ROOT, resume.resume.name))

            data = parser.get_extracted_data()
            resumes_data.append(data)
            resume.name = data.get('name')
            resume.email = data.get('email')
            resume.mobile_number = data.get('mobile_number')
            if data.get('degree') is not None:
                resume.education = ', '.join(data.get('degree'))
            else:
                resume.education = None
            resume.company_name = data.get('company_name')
            resume.college_name = data.get('college_name')
            resume.designation = data.get('designation')
            resume.total_experience = data.get('total_experience')
            if data.get('skills') is not None:
                resume.skills = ', '.join(data.get('skills'))
            else:
                resume.skills = None
            if data.get('experience') is not None:
                resume.experience = ', '.join(data.get('experience'))
            else:
                resume.experience = None
            jobsss = request.POST.get('jobsss')
            jobss = docx2txt.process(os.path.join(settings.MEDIA_ROOT,
                                                  jobsss))

            resume.res = docx2txt.process(
                os.path.join(
                    settings.MEDIA_ROOT, resume.resume.name))

            text = [resume.res, jobss]

            cv = CountVectorizer(lowercase=False)
            count_matrix = cv.fit_transform(text)

            print('Similarity score : ',
                  cosine_similarity(count_matrix))

            matchpercentage = cosine_similarity(count_matrix)[0][1]
            resume.matchpercentage = round(matchpercentage*100, 2)
            print('Your Resume {} % match to the job description !'.format(
                resume.matchpercentage))
            resume.fullname = request.POST['fullname']
            resume.age = request.POST['age']
            resume.exp = request.POST['exp']
            resume.gender = request.POST['gender']
            resume.qo1 = request.POST['qo1']
            resume.qo2 = request.POST['qo2']
            resume.qo3 = request.POST['qo3']
            resume.qo4 = request.POST['qo4']
            resume.qn1 = request.POST['qn1']
            resume.qn2 = request.POST['qn2']
            resume.qn3 = request.POST['qn3']
            resume.qn4 = request.POST['qn4']
            resume.qc1 = request.POST['qc1']
            resume.qc2 = request.POST['qc2']
            resume.qc3 = request.POST['qc3']
            resume.qc4 = request.POST['qc4']
            resume.qa1 = request.POST['qa1']
            resume.qa2 = request.POST['qa2']
            resume.qa3 = request.POST['qa3']
            resume.qa4 = request.POST['qa4']
            resume.qe1 = request.POST['qe1']
            resume.qe2 = request.POST['qe2']
            resume.qe3 = request.POST['qe3']
            resume.qe4 = request.POST['qe4']
            resume.qoi = int((int(resume.qo1)+int(resume.qo2) +
                              int(resume.qo3)+int(resume.qo4))/2.86)
            resume.qni = int((int(resume.qn1)+int(resume.qn2) +
                              int(resume.qn3)+int(resume.qn4))/2.86)
            resume.qci = int((int(resume.qc1)+int(resume.qc2) +
                              int(resume.qc3)+int(resume.qc4))/2.86)
            resume.qai = int((int(resume.qa1)+int(resume.qa2) +
                              int(resume.qa3)+int(resume.qa4))/2.86)
            resume.qei = int((int(resume.qe1)+int(resume.qe2) +
                              int(resume.qe3)+int(resume.qe4))/2.86)
            model = train_model()
            
            expr = request.POST['expr']
            p1 = request.POST['p1']
            p2 = request.POST['p2']

            # expper = int((int(resume.exp)/int(exp))*100)
            p = model.train(resume.qoi, resume.qni, resume.qci,
                            resume.qai, resume.qei, resume.age, resume.gender)

            if p == ['dependable']:
                resume.p = "Dependable"

            elif p == ['serious']:
                resume.p = "Serious"

            elif p == ['responsible']:
                resume.p = "Responsible"

            elif p == ['lively']:
                resume.p = "Lively"

            elif p == ['extraverted']:
                resume.p = "Extraverted"

            if resume.exp >= expr:
                if resume.p == p1 or resume.p == p2:
                    resume.short = 1

            # if expper >= 100:
            #     expper = 100

            # print(expper)

            resume.matching = int(int((int(resume.qoi)+int(resume.qni)+int(resume.qci)+int(
                resume.qai)+int(resume.qei)) + int(resume.matchpercentage))/2)
            if resume.matching >= 100:
                resume.matching = 100

            resume.save()

            return redirect('thankyou')


def home(request, jobid):
    return render(request, jobid, 'main.html')


@login_required(login_url='adlogin_page')
def adminhome(request):
    user = User.objects.all()
    user = request.user.username
    form = job.objects.all()

    return render(request, 'adminhome.html', {'user': user, 'form': form})


def thankyou(request):
    return render(request, 'thankyou.html')


def index(request):
    return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if applicants.objects.filter(username=username).exists():
                messages.info(
                    request, 'This username already exists. Please try again!!')
                return redirect('index')
            else:
                users = applicants(
                    name=name, email=email, username=username, password=password, cpassword=cpassword)
                users.save()
                messages.info(
                    request, 'Account created successfully.')
                return redirect('login_page')
        else:
            messages.info(
                request, 'The Passwords doesnot match. Please try again!!')
            return redirect('index')
    else:
        return redirect('index')


def login_page(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if applicants.objects.filter(username=username).exists() and applicants.objects.filter(password=password).exists():
            messages.success(request, 'Logged in successfully')
            return redirect('availablejobs')
        else:
            messages.info(request, 'Please try again')
            return redirect('login_page')
    else:
        return redirect('login_page')


def adlogin_page(request):
    return render(request, 'adminlogin.html')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('adminhome')
        else:
            messages.info(request, 'Please try again')
            return redirect('adlogin_page')
    else:
        return redirect('adlogin_page')


def mainhome(request):
    return render(request, 'homepage.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def availablejobs(request):
    form = job.objects.all()
    return render(request, 'availablejobs.html', {'form': form})


def apply(request, id):
    jb = job.objects.get(jobid=id)
    return render(request, 'main.html', {'jb': jb})


def gallery(request):
    return render(request, 'gallery.html')


@login_required(login_url='adlogin_page')
def addjob(request):
    return render(request, 'addnewjob.html')


@login_required(login_url='adlogin_page')
def newjob(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job details added successfully')
    else:
        form = DocumentForm()
    return render(request, 'addnewjob.html', {
        'form': form
    })


@login_required(login_url='adlogin_page')
def viewapplicants(request):
    resumes = Resume.objects.all()
    return render(request, 'viewapplicants.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def pyresults(request):
    resumes = Resume.objects.filter(
        jobs='Python Developer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def jvresults(request):
    resumes = Resume.objects.filter(
        jobs='Java Developer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def trresults(request):
    resumes = Resume.objects.filter(
        jobs='Trainer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def teresults(request):
    resumes = Resume.objects.filter(
        jobs='Technician') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def hrresults(request):
    resumes = Resume.objects.filter(
        jobs='HR Excecutive') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def manresults(request):
    resumes = Resume.objects.filter(
        jobs='Sales Manager') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/')
