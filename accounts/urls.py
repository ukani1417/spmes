from django import views
from django.urls import path
from accounts.sys_admin import sys_admin_view
from accounts import views
from django.contrib.auth import views as auth_views
from accounts.student import student_view
from accounts.faculty import faculty_view
from accounts.pgc import pgc_view
urlpatterns = [
    # login & logout
    path('',views.loginpage,name="loginpage"),
    path("logout/",views.logout_request, name= "logout"),

    # Password Reset Urls
    path("password_reset/", views.password_reset_request, name="password_reset"),

    # Admin  urls
    path("sys_admin_faculty/",sys_admin_view.sys_add_faculty,name="sysadmin_add_faculty"),
    path("sys_admin_student/",sys_admin_view.sys_add_student,name="sysadmin_add_student"),

    path('project_types',sys_admin_view.project_types , name="project_types"),
    path('delete/type/<str:pk>',sys_admin_view.delete_type,name="deletedata"),
    path('add/program',sys_admin_view.add_program,name="add_program"),
    path('delete/program/<int:id>',sys_admin_view.delete_program,name="deleteprogram"),
    path('delete/faculty/<str:email>',sys_admin_view.delete_faculty,name="deletefaculty"),
    
    # Pgc
    path("home/", pgc_view.projects, name = "project"),
    path("home/add_project", pgc_view.add_project, name = "add_project"),
    path("home/start_stop_registration/<int:id>", pgc_view.start_stop_registration, name="changestatus"),
    path("home/add_eligible/<int:id>", pgc_view.upload_eligible_list, name="add_eligible"),
    path("home/<int:p_id>/", pgc_view.project_details, name="project_name"),
    path("home/assignments/<int:p_id>/", pgc_view.assignments, name="assignments"),
    path("home/add/assignments/<int:p_id>/", pgc_view.add_assignment, name="add_assignment"),
    path("home/create/committee/<int:p_id>/", pgc_view.examination_committe, name = "committee"),
    path("home/create/add/committee/<int:p_id>/", pgc_view.add_committee, name = "add_committee"),
    path("home/exam/schedule/<int:p_id>/", pgc_view.add_schedule, name = "add_schedule"),
    # path("pgc/create_assignment/<int:p_id>/", pgc_view.create_assignment, name="create_assignment"),


    # student
    path("student/<int:list_id>/",student_view.faculty_list,name="student"),
    path("project/",student_view.eligible_project,name = "student"),
    path("project/append/<int:p_id>/<int:sub_pid>/",student_view.apply,name = "apply"),
    path("project/delete/<int:p_id>/<int:sub_id>/",student_view.delete_request,name = "delete_apply"),
    path("project/groups/<int:p_id>/",student_view.group_details,name = "group_details"),
    path("project/assignments/<int:p_id>/",student_view.submissions,name = "submissions"),
    path("project/assignments/<int:a_id>/<int:p_id>/<int:s_id>/",student_view.upload,name = "upload"),
    path("project/exam/schedule/<int:p_id>/",student_view.exam_schedule,name = "schedule"),
    path("profile/",student_view.profile,name="profile"),
    path("project/certificate/<int:p_id>/",student_view.certificate,name = "certificate"),
    path("project/down_certificate/<int:p_id>/",student_view.dowload_certificate,name = "dowload_certificate"),
    
    # faculty
    path("faculty/",faculty_view.faculties,name="faculty"),
    path("faculty_project/<int:p_id>",faculty_view.faculty_project,name="faculty_project"),
    path("enroll/<int:p_id>/<int:u_id>/",faculty_view.enroll_faculty,name="enroll_faculty"),
    path("faculty/subproject/<int:sp_id>",faculty_view.faculty_sub_project,name="faculty_sub_project"),
    path("faculty/subproject/accept/<int:sp_id>/<int:re_id>",faculty_view.accept_request,name="accept_request"),
    path("faculty/subproject/decline/<int:sp_id>/<int:re_id>",faculty_view.delete_request,name="delete_request"),
    path("faculty/student/groups/<int:sp_id>/",faculty_view.student_groups,name="student_groups"),
    path("faculty/student/AddGroups/<int:sp_id>/",faculty_view.add_group,name="add_group"),
    path("faculty/exam/schedule/<int:p_id>/",faculty_view.exam_schedule,name="exam_schedule"),
    path("faculty/submissions/<int:sp_id>/",faculty_view.get_submission,name="get_submission"),
    path("faculty/submissions/marks/<int:sub_id>/<int:sp_id>/",faculty_view.give_marks,name="give_marks"),
    path("faculty/exam/<int:p_id>",faculty_view.exam,name="exam"),
    path("faculty/assignMarks/<int:p_id>",faculty_view.assign_marks,name="assign_marks"),

    path('excel',pgc_view.export)
]
