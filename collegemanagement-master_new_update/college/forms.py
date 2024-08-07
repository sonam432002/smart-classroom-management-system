from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Classroom,TeacherExtra
#for admin
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


#for student related form
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee','status','year','sem']



#for teacher related form
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['subjects','mobile','status','Department',]




#for Attendance related form

presence_choices = (('Present', 'Present'), ('Absent', 'Absent'))

class AttendanceForm(forms.Form):
    present_status = forms.MultipleChoiceField(
        choices=presence_choices,
        widget=forms.CheckboxSelectMultiple
    )
    date = forms.DateField()
    
class AskDateForm(forms.Form):
    date=forms.DateField()
    




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['subject', 'teacher', 'location', ]



        
# forms.py
from django import forms
from .models import Classroom

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['teacher','subject',  'location', ]
        
from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student_name', 'subject', 'assignment_grade', 'exam_grade', 'project_grade']

from .models import Message,Messageteachrs

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'body']
    
class MessageteachrsForm(forms.ModelForm):
    class Meta:
        model = Messageteachrs
        fields = ['recipient', 'body']    
    
    
# from .models import Timetable
#  # Assuming your TeacherExtra model is defined in teacherextra.py

class TimetableForm(forms.ModelForm):
    class Meta:
        
        fields = [ 'period','day','teacher', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch available subjects and populate choices
        teacher_extra_choices = [(teacher.subjects, teacher.subjects) for teacher in TeacherExtra.objects.all()]
        self.fields['subjects'].widget = forms.Select(choices=teacher_extra_choices)
        
        
        