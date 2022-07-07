
from dataclasses import field
from sre_constants import GROUPREF_EXISTS
# from typing_extensions import Require
from django import forms
from accounts.models import program,faculty,student,sub_project,grp 


# class create_group(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#         self.sub_project_id = kwargs.pop('sub_project_id')
#         sid = forms.ModelMultipleChoiceField(queryset=self.sub_project_id.registred_student.all(), required=False, widget=forms.CheckboxSelectMultiple)
#         class Meta:
#             model = grp
#             exclude = ['student_id','sub_project_id']