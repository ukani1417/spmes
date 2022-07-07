from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from accounts.models import assignment, committee, grp, program,project, project_type, schedule, sub_project, submission, user,student,faculty
from accounts.sys_admin.forms import create_program,student_forms,faculty_forms
from django.contrib import messages

def project_types(request):
    if request.method == "POST":
        add = request.POST.get('addtype')
        if add != '':
            type = project_type(p_type = add)
            type.save()
        return HttpResponseRedirect('project_types')
    else:
        alltypes = project_type.objects.all()
        programs = program.objects.all()
        form = create_program()
        context = {'types':alltypes,'form':form,'programs':programs}
        return render(request, 'sys_admin/project_types.html',context)
    
def delete_type(request,pk):
    if request.method == 'POST':
        pt = project_type.objects.get(id=pk)
        pt.delete()
        return HttpResponseRedirect('/project_types')

@require_POST
def add_program(request):
    form = create_program(request.POST)
    if form.is_valid():
        new_program = program(name = form.cleaned_data['name'], assigned_faculty = form.cleaned_data['assigned_faculty'])
        new_program.save()
        af = new_program.assigned_faculty
        af.is_program_cordinator = True
        af.save()


    return HttpResponseRedirect('/project_types')


def delete_program(request,id):
    if request.method == 'POST': 
        pg = program.objects.get(id = id)
        af = pg.assigned_faculty
        af.is_program_cordinator = False
        af.save()
        pg.delete()
        return HttpResponseRedirect('/project_types')

def sys_add_student(request):
    edit_student_details = student_forms()
    student_details_data = student.objects.all()
    context = {'edit_student_form':edit_student_details,'student_details':student_details_data}
    if request.POST:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please provide CSV type file")
            return render(request, "sys_admin/add_student.html")
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r\n")

        for line in lines:
            fields = line.split(",")
            newuser = user()
            newuser.username = fields[0]
            newuser.set_password(fields[1])
            newuser.email = fields[0]
            newuser.is_active = True
            newuser.is_student = True
            newuser.save()
            newstudent = student()
            newstudent.user = newuser
            temp = fields[0]
            newstudent.sid = temp[:9]
            newstudent.name = fields[2]
            newstudent.program = fields[3]
            newstudent.cpi = 0
            newstudent.save()

        messages.success(request, "Faculty Added Succesfullly")
        return render(request, "sys_admin/add_student.html")
    
    
    return render(request, "sys_admin/add_student.html",context)


def sys_add_faculty(request):
    edit_faculty_details = faculty_forms()
    faculty_details_data = faculty.objects.all()
    context = {'edit_faculty_form':edit_faculty_details,'faculty_details':faculty_details_data}
    if request.POST:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please provide CSV type file")
            return render(request, "sys_admin/add_faculty.html")
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r\n")

        for line in lines:
            fields = line.split(",")
            newuser = user()
            newuser.username = fields[0]
            newuser.set_password(fields[1])
            newuser.email = fields[0]
            newuser.is_active = True
            newuser.is_faculty = True
            newuser.save()
            newfaculty = faculty()
            newfaculty.user = newuser
            newfaculty.name = fields[2]
            newfaculty.save()
        messages.success(request, "Faculty Added Succesfullly")
        return render(request, "sys_admin/add_faculty.html",context)
    
    return render(request, "sys_admin/add_faculty.html",context)


def delete_faculty(request, email):
    user_obj = user.objects.get(username = email)
    faculty_obj = user_obj.faculty
    #delete faculty as user also
    faculty_obj.delete()
    user_obj.delete()
    return redirect('sysadmin_add_faculty')



