from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.models import project,faculty, sub_project, user, student_request, student, grp, grp_map, assignment, submission


def faculties(request):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     fa = request.user.faculty
     enrolled_project_list = fa.enrolled_faculty.all()
     project_list = project.objects.all()
     context = {'enrolled_project_list':enrolled_project_list,'project_list':project_list,'faculty':fa}
     return render(request,"faculty/faculty.html",context)

def faculty_project(request,p_id):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     request.session['p_id'] = p_id
     po = project.objects.get(id = p_id)
     if request.POST:
          if 'del_sp' in request.POST:
                sp = sub_project.objects.get(id = request.POST['sp_id'])
                sp.delete()
                return HttpResponseRedirect(request.path)
          elif 'update' in request.POST:
               sp = sub_project.objects.get(id = request.POST['sp_id'])
               sp.sub_project_area = request.POST['spa']
               sp.sub_project_topic = request.POST['spt']
               sp.max_cap = request.POST['mc']
               if request.FILES:
                    sp.sub_project_pdf = request.FILES['spp']
               
               sp.save()
               return HttpResponseRedirect(request.path)
          else:
               sp = sub_project.objects.create(parent_project = po,related_faculty=request.user.faculty,sub_project_area = request.POST['spa'],sub_project_topic = request.POST['spt'],max_cap = request.POST['mc'])
               if request.FILES:
                    sp.sub_project_pdf = request.FILES['spp']
               sp.save()
               return HttpResponseRedirect(request.path)
               
     spl = sub_project.objects.filter(related_faculty = request.session['user_id']).filter(parent_project = po)
     context = {'po':po, 'spl':spl, 'p_id':p_id}
     return render(request,"faculty/faculty_project.html",context)
    


def enroll_faculty(request,p_id,u_id):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     project_obj = project.objects.get(id = p_id)
     u = user.objects.get(id = u_id)
     project_obj.enrolled_faculty.add(u.faculty)
     project_obj.save()
     return HttpResponseRedirect('/faculty')


def faculty_sub_project(request,sp_id):
     if 'user_id' not in request.session:
          return redirect('loginpage')
     student_list = student_request.objects.filter(status='0').filter(sub_pid=sp_id)
     context = {'student_list':student_list,'sp':sp_id,}
     return render(request,"faculty/faculty_sub_project.html",context)

def accept_request(request,sp_id,re_id):
     sub_proj_obj = sub_project.objects.get(id = sp_id)
     req_obj = student_request.objects.get(id = re_id)
     user_obj = student.objects.get(sid = req_obj.sid)
     user_email = user_obj.user.email
     # parent_obj =
     subject = "Request Accepted"
     email_template_name = "faculty/accepted_request.txt"
     c = {
     "email": user_email,
     'domain': '127.0.0.1:8000',
     'site_name': 'SPMES',
     "user":user_email ,
     "username" : user_obj.name,
     "main_project" : sub_proj_obj.parent_project.name,
     "sub_project_area" : sub_proj_obj.sub_project_area,
     "sub_project_topic" : sub_proj_obj.sub_project_topic,
     "faculty" : sub_proj_obj.related_faculty.name,
     }
     email = render_to_string(email_template_name, c)
     try:
          send_mail(subject, email, 'spmesdaiict@gmail.com',
                         [user_email], fail_silently=False)
     except BadHeaderError:
          messages.error(request,"Invalid header Found")     
     print(req_obj.sid)
     student_obj = student.objects.get(sid = req_obj.sid)
     sub_proj_obj.registred_student.add(student_obj)
     sub_proj_obj.save()
     req_obj.status = 1
     req_obj.save()
     student_request.objects.filter(sid = req_obj.sid).filter(status = -1).delete()
     return redirect("faculty_sub_project",sp_id)

def delete_request(request,sp_id,re_id):
     req_obj = student_request.objects.get(id = re_id)
     print(req_obj)
     active_obj = student_request.objects.filter(sid = req_obj.sid).filter(status = -1).first()
        
     if active_obj is not None:
          active_obj.status = 0
          active_obj.save()
     req_obj.delete()

     return redirect("faculty_sub_project",sp_id)

def student_groups(request,sp_id):
     # sub_projects_list = sub_project.objects.filter(related_faculty = request.session['user_id'])
     group_list = grp.objects.filter(sub_project_id =  sp_id)
     return render(request,"faculty/create_groups.html",{'group_list':group_list,'sp':sp_id})

@require_POST
def add_group(request,sp_id):
     # sub_proj = request.POST.get('sub_project')
     sub = sub_project.objects.get(id = sp_id)
     sid = request.POST.get('sid')
     group_title = request.POST.get('grp_title')
     obj = grp(sub_project_id = sub, student_id = sid, group_title = group_title)
     obj.save()

     ids = sid.split(',')
     ans = ""
     for id in ids:
          ans += id + " | "
          new_obj = grp_map(proj_id = request.session['p_id'], sub_proj_id = sp_id, group_id = obj.id, sid = id)
          new_obj.save()
     ans=ans[:-3]
     obj.student_id = ans
     obj.save() 
     return redirect('student_groups',sp_id)

def exam_schedule(request, p_id):
     proj = project.objects.get(id = p_id)
     sub_proj = sub_project.objects.filter(parent_project = proj)
     lists = []
     for sub_obj in sub_proj:
          lists += list(sub_obj.grp_set.all())
     return render(request, 'faculty/exam_schedule.html',{'groups':lists, 'p_id':p_id})

def get_submission(request,sp_id):
     obj = sub_project.objects.get(id = sp_id)
     grp_list=grp.objects.filter(sub_project_id=obj)
     print(grp_list)
     sub_list=[]
     for list in grp_list:
          print(list.id)
          temp=submission.objects.filter(group_id=list.id)
          print(temp)
          for l in temp:
               stud=list.student_id
               title=list.group_title
               sub_list.append({"list":l,"stud":stud,"title":title})
          print(sub_list)
               # print(l.uploded_time)

     return render(request,'faculty/get_submission.html',{'sub_list':sub_list,'sp':sp_id})

@require_POST
def give_marks(request, sub_id, sp_id):
     obj = submission.objects.get(id = sub_id)
     obj.marks = request.POST.get('marks')
     obj.save()
     return redirect(get_submission,sp_id)

def exam(request, p_id):
     fac_obj = request.user.faculty
    
     committee_obj = fac_obj.in_committee.all()
     
     for it in committee_obj:
          if it.for_project == project.objects.get(id = p_id):
               obj = it
               break
     schedule_list = obj.schedule_set.all()
     print(schedule_list)
     exam_list = []
     for obj in schedule_list:
          subm_obj = submission.objects.filter(group_id = obj.group_id.id)
          sid_list = obj.group_id.student_id.split(' | ')
          marks=[]
          for stud in sid_list:
               markm=grp_map.objects.filter(proj_id=p_id).get(sid=int(stud))
               marks.append({'name': stud ,'mark': markm.marks})
          exam_list.append({'group_title':obj.group_id.group_title, 'faculty':obj.group_id.sub_project_id.related_faculty.name, 'sid':obj.group_id.student_id, 'submissions' : subm_obj,'marks':marks})
     print(exam_list)
     return render(request,"faculty/exam.html",{'exam_list':exam_list, 'p_id':p_id})

@require_POST
def assign_marks(request, p_id):
     sid_list = request.POST.items()
     # print(sid_list)
     cnt = 0
     for keys, values in sid_list:
          if cnt == 0:
               cnt += 1
               continue
          print(keys)
          obj = grp_map.objects.get(proj_id = p_id, sid = keys)
          obj.marks = values
          obj.save()

     return redirect('exam',p_id)