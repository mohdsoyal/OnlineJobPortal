from django import forms
from .models import Jobs , Recruiter

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ("job_title","start_date","end_date","job_salary","experience","location","skill","image","description","created_date")  
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  
            'job_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Your Description','rows':'3'}),
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Experience'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'skill': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Required Skills'}),
            'created_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# forms.py

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['mobile', 'image', 'company', 'company_address']
