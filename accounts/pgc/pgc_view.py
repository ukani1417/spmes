from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from accounts.models import assignment, committee, grp, program,project, project_type, schedule, sub_project, submission, user,student,faculty
from django.contrib import messages
from accounts.pgc.forms import create_project, create_committee, create_assignment, schedule_form
import csv
def projects(request):
    if 'user_id' in request.session:
        project_list = project.objects.all()
        form = create_project()
        context = {'project_list':project_list,'form':form}
        return render(request, 'pgc/index.html',context)
    else:
        return redirect('loginpage')

@require_POST
def add_project(request):
    form = create_project(request.POST)
    if form.is_valid():
        new_project = project(p_type = form.cleaned_data['p_type'], name = form.cleaned_data['name'], start_date = form.cleaned_data['start_date'], end_date = form.cleaned_data['end_date'], status = False)
        new_project.save()
    return HttpResponseRedirect('/home/')

def start_stop_registration(request,id):
    if request.method == 'POST':
        prg = project.objects.get(id=id)
        prg.status = not(prg.status)
        prg.save()
    return HttpResponseRedirect('/home/')

def upload_eligible_list(request,id):
    if request.method == 'POST':
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please provide CSV type file")
            return render(request, "sys_admin/add_student.html")
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r\n")

        list = student.objects.filter(sid__in = lines)
        pr = project.objects.get(id = id)
        for l in list:
            pr.eligible_student.add(l)
            pr.save()
        messages.success(request, "List Uploaded Successfully")

    return HttpResponseRedirect('/home')

def project_details(request, p_id):
    proj = project.objects.get(id = p_id)
    sub_proj = sub_project.objects.filter(parent_project = proj)
    lists = []

    for sub_obj in sub_proj:
        lists += list(sub_obj.grp_set.all())
    context = {'group_list' : lists, 'p_id' : p_id}
    return render(request, "pgc/project_details.html", context)

def export(request):
    response = HttpResponse(content_type = 'text/csv')

    writer = csv.writer(response)
    writer.writerow(['Group ID', 'Student IDs', 'Project Title', 'Faculty name', 'Committee ID', 'Date', 'Time', 'Venue'])

    sub_proj = sub_project.objects.filter(parent_project = 1)
    list = []
    for obj in sub_proj:
        group = obj.grp_set.all()
        for group_obj in group:
            writer.writerow([group_obj.id, str(group_obj.student_id), group_obj.group_title, obj.related_faculty])
            list.append({'first' :obj, 'second':group})
    
    response['Content-Disposition'] = 'attachment; filename="schedule.csv"'
    
    return response

def examination_committe(request, p_id):
    form = create_committee()
    committees = committee.objects.filter(for_project = p_id)
    print(form)
    return render(request, 'pgc/examination_committee.html', {'form':form,'committees':committees,'p_id':p_id})

@require_POST
def add_committee(request,p_id):
    form = create_committee(request.POST)
    if(form.is_valid()):
        for value,text in form.cleaned_data['assigned_faculty']:
            print(text)
    
    # if(form.is_valid()):
    #     new_committee = committee.objects.create(committee_id = 1, for_project = project.objects.get(id = p_id))
    #     new_committee.assigned_faculty.set(form.cleaned_data['assigned_faculty'])
    #     new_committee.save()
    return redirect('committee',p_id)

def assignments(request,p_id):
    obj = project.objects.get(id = p_id)
    assignment_list = assignment.objects.filter(for_project = obj)
    form = create_assignment()
    context = {'assignment_list':assignment_list,'form':form,'p_id':p_id}
    return render(request, 'pgc/assignment.html',context)

@require_POST 
def add_assignment(request,p_id):
    form = create_assignment(request.POST)
    if form.is_valid():
        obj = project.objects.get(id = p_id)
        new_project = assignment(name = form.cleaned_data['name'], deadline = form.cleaned_data['deadline'], total_points = form.cleaned_data['total_points'], weightage = form.cleaned_data['weightage'], for_project = obj)
        new_project.save()
    return redirect('assignments',p_id)

def add_schedule(request,p_id):
    edit_schedule_details = schedule_form()
    proj = project.objects.get(id = p_id)
    sub_proj = sub_project.objects.filter(parent_project = proj)
    lists = []

    for sub_obj in sub_proj:
        lists += list(sub_obj.grp_set.all())
    
    context = {'edit_schedule_details':edit_schedule_details,'groups':lists,'p_id':p_id}
    if request.POST:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please provide CSV type file")
            return render(request, "pgc/exam_schedule.html",context)
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r\n")
        lines.pop(0)
        lines.pop()
        for line in lines:
            fields = line.split(",")
            new_schedule = schedule()
            obj = grp.objects.get(id = fields[0])
            new_schedule.group_id = obj
            committee_obj = committee.objects.get(id = fields[4])
            new_schedule.committee_id = committee_obj
            new_schedule.date = fields[5]
            new_schedule.time = fields[6]
            new_schedule.venue = fields[7]
            new_schedule.save()

        messages.success(request, "Schedule Added Succesfullly")
        return render(request, "pgc/exam_schedule.html",context)
    
    return render(request, "pgc/exam_schedule.html",context)