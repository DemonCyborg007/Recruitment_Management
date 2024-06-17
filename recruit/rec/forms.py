from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import *

class CustomAuthenticationForm(AuthenticationForm):
    pass

class StudentForm(forms.ModelForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['name','enrollment', 'contact', 'email', 'gender', 'city', 'state', 'tenth_grade', 'twelfth_grade', 'resume', 'profile_picture']

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return password2

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = User.objects.create_user(self.cleaned_data['name'], '', self.cleaned_data['enrollment'],is_student=True)  # Empty email for username-based login
        instance.user = user
        if commit:
            instance.save()
        return instance

class FacilitatorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PlacementDriveForm(forms.ModelForm):
    class Meta:
        model = PlacementDrive
        fields = ['company_name', 'job_role', 'eligibility_criteria', 'date']

class BulkUploadForm(forms.Form):
    file = forms.FileField()

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['drive']


### Not tested from here 
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'name', 'enrollment']

    email = forms.EmailField(disabled=True)  # Make the email field read-only

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True  # Ensure email is read-only in the form
