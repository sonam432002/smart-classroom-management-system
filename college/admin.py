from django.contrib import admin
from .models import Attendance,StudentExtra,TeacherExtra,Notice,Resource,ResourceVersion,Subject,Teacher,Classroom,Grade,Message,Messageteachrs,UploadedImage
# Register your models here. (by sumit.luv)
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class ResourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Resource,ResourceAdmin)

class ResourceVersionAdmin(admin.ModelAdmin):
    pass
admin.site.register(ResourceVersion,ResourceVersionAdmin)

class SubjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject,SubjectAdmin)

class TeacherAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teacher,TeacherAdmin)

class ClassroomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Classroom,ClassroomAdmin)

class GradeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Grade,GradeAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message,MessageAdmin)

class MessageteachrsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Messageteachrs,MessageteachrsAdmin)

class UploadedImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(UploadedImage,UploadedImageAdmin)

