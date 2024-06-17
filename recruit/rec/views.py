#for exel file pip install openpyxl
from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
import csv
import pandas as pd

def home(request):
    return render(request, 'rec/home.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_admin:
                messages.info(request, "Logged in as admin.")
                return redirect('admin_dashboard')
            elif user.is_facilitator:
                messages.info(request, "Logged in as facilitator.")
                return redirect('facilitator_dashboard')
            elif user.is_student:
                messages.info(request, "Logged in as student.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "User role is not recognized.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'rec/login.html', {'form': form})
    # if request.method == 'POST':
    #     form = CustomAuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         login(request, user)
    #         if user.is_facilitator:
    #             return redirect('facilitator_dashboard')
    #         elif user.is_student:
    #             return redirect('student_dashboard')
    # else:
    #     form = CustomAuthenticationForm()
    # return render(request, 'rec/login.html', {'form': form})

@login_required
def admin_dashboard(request):
    facilitators = User.objects.filter(is_facilitator=True)
    return render(request, 'rec/admin_dashboard.html', {'facilitators': facilitators})

@login_required
def facilitator_dashboard(request):
    students = Student.objects.all()
    placement_drives = PlacementDrive.objects.all()
    return render(request, 'rec/facilitator_dashboard.html', {'students': students, 'placement_drives': placement_drives})

@login_required
def student_dashboard(request):
    user = request.user
    student = Student.objects.get(user=user)
    placement_drives = PlacementDrive.objects.all()
    return render(request, 'rec/student_dashboard.html', {'student':student,'placement_drives': placement_drives})

@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # user = User.objects.create(username=form.cleaned_data['name'], is_student=True)
            # user.set_password(form.cleaned_data['enrollment'])
            # student = form.save(commit=False)
            # student.user = user
            # student.save()
            return redirect('facilitator_dashboard')
    else:
        form = StudentForm()
    return render(request, 'rec/create_student.html', {'form': form})

@login_required
def create_placement_drive(request):
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST)
        if form.is_valid():
            placement_drive = form.save(commit=False)
            placement_drive.facilitator = request.user
            placement_drive.save()
            return redirect('facilitator_dashboard')
    else:
        form = PlacementDriveForm()
    return render(request, 'rec/create_placement_drive.html', {'form': form})

@login_required
def create_facilitator(request):
    if request.method == 'POST':
        form = FacilitatorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_password(form.cleaned_data['password'])
            user.is_facilitator = True
            user.save()
            return redirect('admin_dashboard')
    else:
        form = FacilitatorForm()
    return render(request, 'rec/create_facilitator.html', {'form': form})

def bulk_upload_students(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                data = csv.DictReader(file.read().decode('utf-8').splitlines())
                for row in data:
                    create_student_by_row(row,is_excel=False)
                    messages.success(request, 'Student ' + row['name'] + ' added successfully.')
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
                for _, row in data.iterrows():
                    create_student_by_row(row,is_excel=True)
                    messages.success(request, 'Student ' + row['name'] + ' added successfully.')
            else:
                messages.error(request, 'Unsupported file format. Please upload a CSV or Excel file.')
            # return redirect('facilitator_dashboard')
    else:
        form = BulkUploadForm()
    return render(request, 'rec/bulk_upload.html', {'form': form})

def create_student_by_row(row,is_excel=False):
    user = User.objects.create_user(
        username=row['name'],
        email=row['email'],
        password=row['enrollment'],  # Set enrollment number as default password
        is_student=True
    )
    Student.objects.create(
        user=user,
        name=row['name'] ,
        enrollment=row['enrollment'],
        contact=row['contact'],
        email=row['email'] ,
        gender=row['gender'] ,
        city=row['city'] ,
        state=row['state'] ,
        tenth_grade=row['tenth_grade'] ,
        twelfth_grade=row['twelfth_grade'] 
    )


@login_required
def apply_to_placement_drive(request, drive_id):
    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.drive = drive
            application.save()
            return redirect('student_dashboard')
    else:
        form = ApplicationForm(initial={'drive': drive})
    return render(request, 'rec/apply_to_drive.html', {'form': form, 'drive': drive})

@login_required
def student_application_history(request):
    applications = Application.objects.filter(student=request.user)
    return render(request, 'rec/student_application_history.html', {'applications': applications})

@login_required
def view_student_applications(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    applications = Application.objects.filter(student=student.user)
    return render(request, 'rec/view_student_applications.html', {'student': student, 'applications': applications})
    


############################
### Not Tested from here ###
############################
@login_required
def update_student_profile(request):
    student = get_object_or_404(Student, user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'rec/update_student_profile.html', {'form': form})
