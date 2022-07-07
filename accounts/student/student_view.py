
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from accounts.models import student,faculty, student_request,user,project,sub_project,grp_map, grp, submission, assignment
from django.contrib import messages
from django.template.loader import render_to_string
from weasyprint import HTML, CSS

def eligible_project(request):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     stud=request.user.student
     eligible_list=stud.project.all()
     context = {'eligible_list':eligible_list}
     return render(request,"student/student.html",context)

def faculty_list(request,list_id):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     request.session['p_id'] = list_id

     # parent project 
     parent_obj = project.objects.get(id = list_id)

     # check in registre student
     is_reg = student_request.objects.filter(sid = request.session['sid']).filter(status=1).exists()
     print(is_reg,parent_obj)
     list = project.objects.get(id=list_id)
     fac_list=list.sub_project_set.all().order_by('related_faculty') 
     app_list = student_request.objects.filter( sid = request.session['sid'])
     count=[] 
     for i in fac_list:
          count.append(student_request.objects.filter(sub_pid=i.id).count())
     count2=[] 
     for i in app_list:
          count2.append(sub_project.objects.get(id=i.sub_pid))
     return render(request,"student/list_faculty.html",context = {'all':zip(fac_list,count),'app_list':zip(app_list,count2),'parent_obj':parent_obj,'is_reg':is_reg,'p_id':list_id})

def apply(request,p_id, sub_pid):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     request.session['sub_project_id'] = sub_pid
     if not student_request.objects.filter(sid = request.session['sid']).filter(sub_pid = sub_pid).exists():
          check = student_request.objects.filter(sid = request.session['sid']).exists()
          # if student id is not in request list status is active else pending
          if not check:
               obj = student_request(sub_pid = sub_pid, sid = request.session['sid'], status = 0)
               obj.save()
          else:
               obj = student_request(sub_pid = sub_pid, sid = request.session['sid'], status = -1)
               obj.save()
          return redirect('student',p_id)
     else:
          messages.info(request,"Already applied")
          return redirect('student',p_id)

def delete_request(request,p_id, sub_id):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     obj = student_request.objects.get(id = sub_id)

     if obj.status == 0:
          active_obj = student_request.objects.filter(sid = obj.sid).filter(status = -1).first()
          if active_obj is not None:
               active_obj.status = 0
               active_obj.save()
          obj.delete()
          messages.info(request, "Request removed")
          return redirect('student',p_id)
     else:
          obj.delete()
          messages.info(request, "Request removed")
          return redirect('student',p_id)

def group_details(request, p_id):
     obj = grp_map.objects.filter(proj_id = p_id).filter(sid = request.session['sid']).first()
     group = grp.objects.get(id = obj.group_id)
     ids = group.student_id.split(',')
     return render(request, 'student/group.html', {'group':group,'ids':ids, 'p_id':p_id})

def  submissions(request,p_id):
     obj = project.objects.get(id = p_id)
     assignment_list = assignment.objects.filter(for_project = obj)
     grp_obj = grp_map.objects.get(proj_id = p_id, sid = request.session['sid'])
     submissions = submission.objects.filter(group_id = grp_obj.group_id)
     print(submissions)
     context = {'assignment_list':assignment_list,'submissions':submissions, 'p_id':p_id}
     return render(request, 'student/submissions.html',context)

def upload(request,a_id,p_id,s_id):
     if request.method == "POST":
          grpid=grp_map.objects.filter(proj_id=p_id).get(sid=s_id)
          try:
               obj = submission.objects.get(assignment_id=assignment.objects.get(id=a_id),group_id=grpid.group_id)
               obj.sub_pdf_name.delete()
               obj.sub_pdf_name=request.FILES['document']
               obj.save()
          except submission.DoesNotExist:
               obj=submission(assignment_id=assignment.objects.get(id=a_id),group_id=grpid.group_id,marks=0,sub_pdf_name=request.FILES['document'])
               obj.save()
     return redirect('submissions',p_id)

def exam_schedule(request,p_id):
     proj = project.objects.get(id = p_id)
     sub_proj = sub_project.objects.filter(parent_project = proj)
     lists = []
     for sub_obj in sub_proj:
          lists += list(sub_obj.grp_set.all())
     return render(request, 'student/exam_schedule.html',{'groups':lists, 'p_id':p_id})

def profile(request):
     student_obj = request.user.student
     if request.POST:
          student_obj.cpi = request.POST['cpi']
          student_obj.save()
          return HttpResponseRedirect(request.path)
     context = {'student_obj':student_obj}
     return render(request,"student/profile.html",context)

def certificate(request,p_id):


    

     student_obj = request.user.student
     pro_obj = project.objects.get(id = p_id)
     sp_proj_obj= student_obj.registred_project.get(parent_project = pro_obj)
     # sp_id= student_request.objects.get(sid=student_obj.sid,status=1)
     # sp_proj_obj = sub_project.objects.get(id=sp_id.sub_pid)
     faculty_obj = sp_proj_obj.related_faculty
     grp_map_obj = grp_map.objects.get(sub_proj_id = sp_proj_obj.id,proj_id=p_id,sid=student_obj.sid)
     grp_size = grp_map.objects.filter(group_id= grp_map_obj.group_id).count()
     # print(pro_obj,sp_proj_obj,grp_map_obj)

     
     
     student_submission_marks = submission.objects.filter(group_id = grp_map_obj.group_id)
     result = {'sid':student_obj.sid,'title':pro_obj.name,'submission':student_submission_marks,'viva_marks':grp_map_obj.marks,'final_marks':grp_map_obj.final_marks}
     context = {'p_id':p_id,'mp_title':pro_obj.name,'faculty':faculty_obj.name,
                'marks':grp_map_obj.marks,
                'student':student_obj,'result':result,'project':pro_obj.name,
                'sub_project':sp_proj_obj,'size':grp_size,
                'startdate':pro_obj.start_date,'enddate':pro_obj.end_date}
     return render(request,'student/certificate.html',context)   

def dowload_certificate(request,p_id):
     student_obj = request.user.student
     pro_obj = project.objects.get(id = p_id)
     sp_proj_obj= student_obj.registred_project.get(parent_project = pro_obj)
     faculty_name = sp_proj_obj.related_faculty.name
     grp_map_obj = grp_map.objects.get(sub_proj_id = sp_proj_obj.id,proj_id=p_id,sid=student_obj.sid)
     grp_size = grp_map.objects.filter(group_id= grp_map_obj.group_id).count()
     student_submission_marks = submission.objects.filter(group_id = grp_map_obj.group_id)
     context = {'p_id':p_id,'mp_title':pro_obj.name,'faculty':faculty_name,
                'marks':grp_map_obj.marks,
                'student':student_obj,'project':pro_obj.name,
                'sub_project':sp_proj_obj,'size':grp_size,
                'startdate':pro_obj.start_date,'enddate':pro_obj.end_date}
     if request.POST:
          html_page = render_to_string('student/cer_temp.html',context)
          # Html_template = get_template('student/cer_temp.html')
          pdf_file = HTML(string=html_page, base_url='base_url').write_pdf(stylesheets=[CSS(string='@page { size:  landscape;}')])
          response = HttpResponse(pdf_file, content_type='application/pdf')
          response['Content-Disposition'] = 'filename="home_page.pdf"'
          return response