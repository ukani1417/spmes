from django.contrib import admin
from accounts.models import assignment, committee, grp, grp_map, program,project, project_type, schedule, sub_project, submission, user,student,faculty, student_request
# Register your models here.

class student_request_admin(admin.ModelAdmin):
    fields= [
        'time_stamp','sid','sub_pid','status'
        ]
    readonly_fields= [ 'time_stamp' ]
    list_display = ('time_stamp','sid','sub_pid','status')
    class Meta:
        model=student_request

class submission_admin(admin.ModelAdmin):
    fields= [
        'time_stamp','assignment_id','group_id','sub_pdf_name','marks'
        ]
    readonly_fields= [ 'time_stamp' ]
    list_display = ('time_stamp','assignment_id','group_id','sub_pdf_name','marks')
    class Meta:
        model=submission


admin.site.register(user)
admin.site.register(student)
admin.site.register(faculty)
admin.site.register(project)
admin.site.register(project_type)
admin.site.register(sub_project)
admin.site.register(grp)
admin.site.register(assignment)
admin.site.register(program)
admin.site.register(committee)
admin.site.register(submission,submission_admin)
admin.site.register(schedule)
admin.site.register(student_request,student_request_admin)
admin.site.register(grp_map)
