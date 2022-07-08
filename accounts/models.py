
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


# for admin
class user(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class student(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,primary_key=True)
    sid = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=50)
    cpi = models.FloatField()
    
    def __str__(self):
        return self.sid


class faculty(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100)
    is_exminer = models.BooleanField(default=False)
    is_program_cordinator = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# admin
class project_type(models.Model):
    p_type = models.CharField(max_length=250)

    def __str__(self):
        return self.p_type

#program cordinator
class program(models.Model):
    name = models.CharField(max_length=250)
    assigned_faculty = models.OneToOneField(faculty,on_delete = models.CASCADE)

    def __str__(self):
        return self.name



# admin
class project(models.Model):
    p_type = models.ForeignKey(project_type,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=False)
    eligible_student = models.ManyToManyField(student,related_name='project', blank=True)
    enrolled_faculty = models.ManyToManyField(faculty,related_name='enrolled_faculty',blank=True)
    def __str__(self):
        return self.name
        
# faculty
class sub_project(models.Model):
    parent_project = models.ForeignKey(project,on_delete=models.CASCADE)
    related_faculty = models.ForeignKey(faculty,on_delete=models.CASCADE)
    registred_student = models.ManyToManyField(student,related_name='registred_project',blank=True)
    sub_project_area = models.CharField(max_length=200)
    sub_project_topic = models.CharField(max_length=200)
    sub_project_pdf = models.FileField(upload_to='sub_project/',blank=True)
    max_cap = models.IntegerField()
    def __str__(self):
        return self.sub_project_topic   
    def delete(self,*args, **kwargs):
        if self.sub_project_pdf:
            self.sub_project_pdf.delete()
        super().delete(*args,**kwargs)

class student_request(models.Model):
    sub_pid = models.IntegerField()
    sid = models.IntegerField()
    status = models.IntegerField(default=-1)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sid)
    

class grp(models.Model):
    sub_project_id = models.ForeignKey(sub_project,on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100)
    group_title = models.CharField(max_length=250)

    def __str__(self):
        return self.group_title



class assignment(models.Model):
    name = models.CharField(max_length=100)
    deadline = models.DateField()
    total_points = models.IntegerField()
    weightage = models.IntegerField()
    for_project = models.ForeignKey(project,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class submission(models.Model):
    assignment_id = models.ForeignKey(assignment,on_delete=models.CASCADE)
    group_id = models.IntegerField()
    marks = models.IntegerField()
    sub_pdf_name = models.FileField(upload_to="submissions/")
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sub_pdf_name.name)

class committee(models.Model):
    committee_id = models.IntegerField()
    for_project = models.ForeignKey(project,on_delete=models.CASCADE)
    assigned_faculty = models.ManyToManyField(faculty,related_name='in_committee')

    def __str__(self):
        return str(self.committee_id)

class schedule(models.Model):
    group_id = models.OneToOneField(grp,on_delete=models.CASCADE)
    committee_id = models.ForeignKey(committee,on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    venue = models.CharField(max_length=250)
    time = models.CharField(max_length=100)

    def __str__(self):
        return str(self.group_id)

class grp_map(models.Model):
    proj_id = models.IntegerField()
    sub_proj_id = models.IntegerField()
    group_id = models.IntegerField()
    sid = models.CharField(max_length=100)
    marks = models.FloatField(default=0)
    final_marks = models.FloatField(default=0)