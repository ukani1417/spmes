from tkinter import Widget
from django import forms

from accounts.models import project, committee,faculty, assignment, schedule


class create_project(forms.ModelForm):
    class Meta:
        model = project
        fields = ['p_type','name','start_date','end_date']
        widgets = {
            'p_type' : forms.Select(attrs={'class':'form-select', 'placeholder':'Project Type'}),
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Project Name'}),
            'start_date' : forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'end_date' : forms.DateInput(format=('%d-%m-%Y'),attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
        }

class create_committee(forms.ModelForm):

    assigned_faculty = forms.ModelMultipleChoiceField(queryset=faculty.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = committee
        exclude = ['for_project','committee_id']
        widgets = {
            'committee_id' : forms.NumberInput(attrs={'class':'form-control','placeholder':''})
        }
        

class create_assignment(forms.ModelForm):
    class Meta:
        model = assignment
        fields = '__all__'
        exclude = ['for_project']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Assignment Name'}),
            'deadline' : forms.DateInput(format=('%d-%m-%Y'),attrs={'class':'form-control','type': 'date'}),
            'total_points' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Total points'}),
            'weightage' : forms.NumberInput(attrs={'class':'form-control','placeholder':'Weightage'})
        }

class schedule_form(forms.ModelForm):
    class Meta:
        model = schedule
        fields = '__all__'
