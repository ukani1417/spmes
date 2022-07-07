# from django import forms
# from accounts.models import user
# from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# from django.db import transaction


# # class ucs(UserCreationForm):
# #     class Meta:
# #         model = user
# #         fields = ('username','email','is_student','is_faculty','is_admin',)

# # class uxf(UserChangeForm):
# #     class Meta:
# #         model = user
# #         fields = ('username','email','is_student','is_faculty','is_admin',)

# # class studentregistrationform(ucs):
# #     sid = forms.CharField(max_length=9,min_length=9,required=True)
# #     name = forms.CharField(max_length=9,required=True)
# #     program = forms.CharField(max_length=50,required=True)
# #     cpi = forms.FloatField()

    
# #     class Meta(ucs.Meta):
# #         model=user

# #     @transaction.atomic
# #     def save(self):
# #         new_user = super().save(commit=False)
# #         new_user.email=self.cleaned_data.get('email')
# #         new_user.is_student = True
# #         new_user.save()
# #         student = student.objects.create(user=user)
# #         student.sid = self.cleaned_data.get('sid')


# #         return user

# # class facultyregistrationform(ucs):
# #     name = forms.CharField(max_length=100,required=True)
# #     is_exminer = forms.BooleanField()
# #     is_program_cordinator = forms.BooleanField()
    
# #     class Meta(ucs.Meta):
# #         model=user


from dataclasses import field
from django import forms
from accounts.models import program,faculty,student

class create_program(forms.ModelForm):
    class Meta:
        model = program
        fields = ['name','assigned_faculty']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Program Name',}),
            'assigned_faculty' : forms.Select(attrs={'class':'form-select ','placeholder':'Assigned Faculty',})
        }

class faculty_forms(forms.ModelForm):
    class Meta:
        model = faculty
        fields = '__all__'

class student_forms(forms.ModelForm):
    class Meta:
        model = student
        fields = '__all__'