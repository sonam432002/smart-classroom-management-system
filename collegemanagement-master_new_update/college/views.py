from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from .models import Notice

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/index.html')



#for showing signup/login button for teacher(by 
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/adminclick.html')


#for showing signup/login button for teacher(by 
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/teacherclick.html')


#for showing signup/login button for student(by 
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'college/studentclick.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'college/adminsignup.html',{'form':form})




def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'college/studentsignup.html',context=mydict)


def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'college/teachersignup.html',context=mydict)






#for checking user is techer , student or admin(by )
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'college/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'college/student_wait_for_approval.html')




#for dashboard of adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by )

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

    teachersubjects=models.TeacherExtra.objects.filter(status=True).count()
    # pendingteachersalary=models.TeacherExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentDepartment=models.StudentExtra.objects.filter(status=True).count()
    # pendingstudentfee=models.StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay(by )
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        # 'teachersalary':teachersalary['salary__sum'],
        # 'pendingteachersalary':pendingteachersalary['salary__sum'],

        # 'studentfee':studentfee['fee__sum'],
        # 'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'college/admin_dashboard.html',context=mydict)







#for teacher sectionnnnnnnn by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by )

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'college/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'college/admin_add_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'college/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=False)
    return render(request,'college/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'college/admin_update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'college/admin_view_teacher_salary.html',{'teachers':teachers})






#for student by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(by )

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'college/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'college/admin_add_student.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'college/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'college/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'college/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'college/admin_view_student_fee.html',{'students':students})






#attendance related viewwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww(by 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'college/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'college/admin_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'college/admin_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'college/admin_view_attendance_ask_date.html',{'cl':cl,'form':form})









#fee related view by adminnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn(
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'college/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'college/admin_view_fee.html',{'feedetails':feedetails,'cl':cl})








#notice related viewsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss(by 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'college/admin_notice.html',{'form':form})


def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == 'POST':
        notice.delete()
        return redirect('admin-dashboard')
    return render(request, 'college/delete_notice.html', {'notice': notice})   

def student_delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == 'POST':
        notice.delete()
        return redirect('student-dashboard')
    return render(request, 'college/student_delete_notice.html', {'notice': notice}) 







#for TEACHER  LOGIN    SECTIONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN(by 
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        # 'salary':teacherdata[0].salary,
         'subjects':teacherdata[0].subjects,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
       
    }
    return render(request,'college/teacher_dashboard.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'college/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'college/teacher_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'college/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'college/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'college/teacher_notice.html',{'form':form})

def teacher_delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == 'POST':
        notice.delete()
        return redirect('teacher-dashboard')
    return render(request, 'college/teacher_delete_notice.html', {'notice': notice}) 





#FOR STUDENT AFTER THEIR Loginnnnnnnnnnnnnnnnnnnnn(by 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice
    }
    return render(request,'college/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'college/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'college/student_view_attendance_ask_date.html',{'form':form})









# for aboutus and contact ussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss (by 
def aboutus_view(request):
    return render(request,'college/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'college/contactussuccess.html')
    return render(request, 'college/contactus.html', {'form':sub})
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# new add 
from .models import Resource

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def resource_management(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        uploaded_by = request.user
        resource = Resource.objects.create(title=title, description=description, file=file, uploaded_by=uploaded_by)
        return redirect('resource_management')
    
    

    resources = Resource.objects.all()
    return render(request, 'college/resource_management.html', {'resources': resources})

# add by  new page for add coausr details teach-resorce section 

@user_passes_test(is_teacher)
def delete_resource(request, pk):
    resource = Resource.objects.get(pk=pk)
    if request.method == 'POST':
        resource.delete()
    return redirect('resource_management')

def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    file_path = resource.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={resource.file.name}'
        return response
    



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'college/student_resource.html', {'resources': resources})



# # views.py

from .models import Classroom
from .forms import ClassroomForm

# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher) # Ensure the user is logged in
# def schedule_and_view_classes(request):
#     if request.method == 'POST':
#         location = request.POST.get('location')
#         start_time = request.POST.get('start_time')
#         end_time = request.POST.get('end_time')
#         # Assuming you have a Teacher object to associate with the class
#         # You would typically associate the logged-in teacher with the class
#         # Replace 'teacher' with your actual logic to get the current teacher
#         teacher = request.user.teacher  # Assuming a one-to-one relationship between User and Teacher
        
#         # Create Classroom instance
#         new_classroom = Classroom.objects.create(
#             location=location,
#             start_time=start_time,
#             end_time=end_time,
#             teacher=teacher
#         )
#         new_classroom.save()
        
#     # Fetch all classes
#     classes = Classroom.objects.all()
    
#     return render(request, 'college/schedule_and_view_classes.html', {'classes': classes})



# from .models import Classroom
# from .forms import ScheduleForm
# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher)
# def schedule_and_view_classes(request):
#     if request.method == 'POST':
#         form = ScheduleForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             location = form.cleaned_data['location']
#             start_time = form.cleaned_data['start_time']
#             end_time = form.cleaned_data['end_time']
#             teacher = request.user.teacher

#             # Create Classroom instance
#             new_classroom = Classroom.objects.create(
#                 # subject=subject,
#                 location=location,
#                 start_time=start_time,
#                 end_time=end_time,
#                 teacher=teacher
#             )
#             new_classroom.save()
#             return redirect('schedule_and_view_classes')

#     else:
#         form = ScheduleForm()

#     # Fetch all classes
#     classes = Classroom.objects.all()

#     return render(request, 'college/schedule_and_view_classes.html', {'form': form, 'classes': classes})

from .forms import ScheduleForm
from datetime import datetime

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def schedule_and_view_classes(request):
    # Assuming the logged-in user is a teacher
    teacher = request.user.teacherextra  # Assuming the related name is 'teacherextra'

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            # Extract date and time values from form data
            start_date = request.POST.get('start_date')
            start_time = request.POST.get('start_time')
            end_date = request.POST.get('end_date')
            end_time = request.POST.get('end_time')

            # Convert date and time strings to datetime objects
            start_datetime = datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(end_date + ' ' + end_time, '%Y-%m-%d %H:%M')

            # Save form data along with extracted date and time values
            new_class = form.save(commit=False)
            new_class.start_time = start_datetime
            new_class.end_time = end_datetime
            new_class.teacher = teacher  # Assign the logged-in teacher to the class
            new_class.save()

            return redirect('schedule_and_view_classes')

    else:
        # Initialize the form with initial values for teacher and subject
        initial_data = {'teacher': teacher.get_name, 'subject': teacher.subjects}
        form = ScheduleForm(initial=initial_data)

    # Fetching classes only for the logged-in teacher
    classes = Classroom.objects.filter(teacher=teacher)

    return render(request, 'college/schedule_and_view_classes.html', {'form': form, 'classes': classes})

# student see shedule timimig by teacher

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_schedule_and_view_classes(request):
    
       

    classes = Classroom.objects.all()
    return render(request, 'college/student_schedule_and_view_classes.html', {'classes': classes})

# for grading system
# from django.shortcuts import render, redirect
# from .models import Teacher, Student, Grade, Assignment, Exam, Project,Course
# from .forms import GradeForm

# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher)
# def gradebook(request):
#     if request.user.is_authenticated:
#         if request.user.teacher.method == 'GET':
#             teacher = Teacher.objects.get(user=request.user)
#             courses = Course.objects.filter(teacher=teacher)
#             return render(request, 'college/teacher_gradebook.html', {'courses': courses})
#         else:
#             student = Student.objects.get(user=request.user)
#             grades = Grade.objects.filter(student=student)
#             return render(request, 'college/student_grades.html', {'grades': grades})
    

# def input_grade(request, assessment_type, assessment_id):
#     if request.method == 'POST':
#         form = GradeForm(request.POST)
#         if form.is_valid():
#             grade = form.save(commit=False)
#             if assessment_type == 'assignment':
#                 grade.assignment_id = assessment_id
#             elif assessment_type == 'exam':
#                 grade.exam_id = assessment_id
#             elif assessment_type == 'project':
#                 grade.project_id = assessment_id
#             grade.student = Student.objects.get(user=request.user)
#             grade.save()
#             return redirect('gradebook')
#     else:
#         form = GradeForm()
#     return render(request, 'college/input_grade.html', {'form': form})

# def update_grade(request, grade_id):
#     grade = Grade.objects.get(pk=grade_id)
#     if request.method == 'POST':
#         form = GradeForm(request.POST, instance=grade)
#         if form.is_valid():
#             form.save()
#             return redirect('gradebook')
#     else:
#         form = GradeForm(instance=grade)
#     return render(request, 'college/update_grade.html', {'form': form})
# views.py
# from django.shortcuts import render, redirect
# from .models import Assignment, Exam, Project, Grade
# from .forms import GradeForm

# def teacher_gradebook(request):
#     assignments = Assignment.objects.all()
#     exams = Exam.objects.all()
#     projects = Project.objects.all()
#     context = {
#         'assignments': assignments,
#         'exams': exams,
#         'projects': projects,
#     }
#     return render(request, 'college/teacher_gradebook.html', context)

# def update_grade(request, grade_id):
#     grade = Grade.objects.get(id=grade_id)
#     form = GradeForm(instance=grade)
#     if request.method == 'POST':
#         form = GradeForm(request.POST, instance=grade)
#         if form.is_valid():
#             form.save()
#             return redirect('teacher_gradebook')
#     context = {
#         'form': form,
#     }
#     return render(request, 'college/update_grade.html', context)

# def student_grades(request):
#     student = request.user.student
#     grades = Grade.objects.filter(student=student)
#     context = {
#         'grades': grades,
#     }
#     return render(request, 'college/student_grades.html', context)
from django.shortcuts import render, redirect
from .models import Grade
from .forms import GradeForm

# def update_grade(request, grade_id):
#     grade = Grade.objects.get(id=grade_id)
#     form = GradeForm(instance=grade)
#     if request.method == 'POST':
#         form = GradeForm(request.POST, instance=grade)
#         if form.is_valid():
#             form.save()
#             return redirect('teacher_gradebook')
#     context = {
#         'form': form,
#     }
#     return render(request, 'college/update_grade.html', context)

# def teacher_gradebook(request):
#     grades = Grade.objects.all()
#     context = {
#         'grades': grades,
#     }
#     return render(request, 'college/teacher_gradebook.html', context)

# def student_grades(request):
#     student = request.user.student
#     grades = Grade.objects.filter(student=student)
#     context = {
#         'grades': grades,
#     }
#     return render(request, 'college/student_grades.html', context)

from django.shortcuts import render
from .models import Grade
from .forms import GradeForm



# def teacher_gradebook(request):
    
#     grades = Grade.objects.all()
#     form = GradeForm()
       
#     context = {
#         'grades': grades,
#         'form': form,
#         }
    
#     return render(request, 'college/teacher_gradebook.html', context)



# @login_required(login_url='teacherlogin')
# @user_passes_test(is_teacher)
# def teacher_gradebook(request):
#     if request.method == 'POST':
#         form = GradeForm(request.POST)
#         if form.is_valid():
#             form.save()  # This will automatically create and save the Grade object
            
#             # Redirect to a success page or the same page (to prevent form resubmission)
#             return redirect('teacher_gradebook')
#     else:
#         form = GradeForm()
    
#     # Fetch all Grade objects from the database
#     grades = Grade.objects.all()
    
#     return render(request, 'college/teacher_gradebook.html', {'form': form, 'grades': grades})

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)  # Assuming you have this custom user check function
def teacher_gradebook(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()  # This will automatically create and save the Grade object
            return redirect('teacher_gradebook')  # Redirect to prevent form resubmission
    else:
        form = GradeForm()
    
    # Fetch all Grade objects from the database
    grades = Grade.objects.all()
    
    return render(request, 'college/teacher_gradebook.html', {'form': form, 'grades': grades})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Grade
from .models import TeacherExtra
from django.core import serializers

def update_grade(request, grade_id):
    if request.method == 'POST':
        data = request.POST
        try:
            grade = Grade.objects.get(pk=grade_id)
            
            # Retrieve grades from POST data
            assignment_grade = data.get('assignment_grade')
            exam_grade = data.get('exam_grade')
            project_grade = data.get('project_grade')
            
            # Validate grades (ensure they are numeric)
            if not (assignment_grade.isdigit() and exam_grade.isdigit() and project_grade.isdigit()):
                return JsonResponse({'success': False, 'error': 'Invalid grades. Grades must be numeric.'})
            
            # Convert grades to integers
            assignment_grade = int(assignment_grade)
            exam_grade = int(exam_grade)
            project_grade = int(project_grade)

            # Update grades
            grade.update_grades(assignment_grade, exam_grade, project_grade)

            # Serialize updated grade object to JSON
            updated_grade_json = serializers.serialize('json', [grade])
            return JsonResponse({'success': True, 'updated_grade': updated_grade_json})
        except Grade.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Grade not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

import json
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_messaging(request):
    teachers = TeacherExtra.objects.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Get the selected teacher's ID from the form
            teacher_id = form.cleaned_data['recipient'].id
            # Get the selected teacher object
            selected_teacher = TeacherExtra.objects.filter(id=teacher_id).first()
            if selected_teacher:
                # Get the current student
                sender = request.user.studentextra
                # Create a new message object
                message = Message(
                    sender=sender,
                    recipient=selected_teacher,
                    body=form.cleaned_data['body']
                )
                # Save the message to the database
                message.save()
                # Redirect to the same page to refresh and display new messages
                return redirect('student_messaging')
    else:
        form = MessageForm()
    
    # Get all messages sent by the current student
    student_messages = Message.objects.filter(sender=request.user.studentextra)
    
    # Get all messages received by the current student from teachers
    teacher_messages = Messageteachrs.objects.filter(recipient=request.user.studentextra)
    
    return render(request, 'college/student_messaging.html', {'form': form, 'teachers': teachers, 'teacher_messages': teacher_messages, 'student_messages': student_messages})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeacherExtra,StudentExtra, Message,Messageteachrs
from .forms import MessageForm,MessageteachrsForm


from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test




@login_required(login_url='teacherlogin')
def teacher_reply(request):
    students = StudentExtra.objects.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Get the selected student's ID from the form
            student_id = form.cleaned_data['recipient'].id
            # Get the selected student object
            selected_student = StudentExtra.objects.filter(id=student_id).first()
            if selected_student:
                # Get the current teacher
                sender = request.user.teacherextra
                # Create a new message object
                message = Messageteachrs(
                    sender=sender,
                    recipient=selected_student,
                    body=form.cleaned_data['body']
                )
                # Save the message to the database
                message.save()
                # Redirect to the same page to refresh and display new messages
                return redirect('teacher_reply')
    else:
        form = MessageteachrsForm()
    
    # Get all messages sent by the current teacher
    teacher_messages = Messageteachrs.objects.filter(sender=request.user.teacherextra)
    
    # Get all messages received by the current teacher from students
    student_messages = Message.objects.filter(recipient=request.user.teacherextra)
    
    return render(request, 'college/teacher_reply.html', {'form': form, 'students': students, 'teacher_messages': teacher_messages, 'student_messages': student_messages})






from django.core.files.storage import FileSystemStorage
from .models import UploadedImage

def admin_timetable(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        image_object = UploadedImage.objects.create(image=uploaded_image)
    uploaded_images = UploadedImage.objects.all()
    return render(request, 'college/admin_timetable.html', {'uploaded_images': uploaded_images})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        image_object = UploadedImage.objects.create(image=uploaded_image)
    uploaded_images = UploadedImage.objects.all()
    return render(request, 'college/admin_timetable.html', {'uploaded_images': uploaded_images})

def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)
    if request.method == 'POST':
        image.delete()
    return redirect('upload_image')


@login_required(login_url='adminlogin')
def admin_resource_mangment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        uploaded_by = request.user
        resource = Resource.objects.create(title=title, description=description, file=file, uploaded_by=uploaded_by)
        return redirect('admin_resorce_mangment')
    
    

    resources = Resource.objects.all()
    return render(request, 'college/admin_resorce_mangment.html',{'resources': resources})


# @user_passes_test(is_admin)
def delete_resource(request, pk):
    resource = Resource.objects.get(pk=pk)
    if request.method == 'POST':
        resource.delete()
    return redirect('admin_resorce_mangment')


def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    file_path = resource.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={resource.file.name}'
        return response

@login_required(login_url='adminlogin')
def admin_gradebook(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()  # This will automatically create and save the Grade object
            return redirect('admin_gradebook')  # Redirect to prevent form resubmission
    else:
        form = GradeForm()
    
    # Fetch all Grade objects from the database
    grades = Grade.objects.all()
    
    return render(request, 'college/admin_gradebook.html', {'form': form, 'grades': grades})
    

def admin_messaging(request):
    
   from django.contrib.auth.models import User
from .models import Message, TeacherExtra, StudentExtra

def admin_messaging(request):
    all_messages = Message.objects.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient_id = form.cleaned_data['recipient'].id
            recipient_type = form.cleaned_data['recipient_type']
            recipient = None
            
            # Determine the recipient based on the selected recipient type
            if recipient_type == 'teacher':
                recipient = TeacherExtra.objects.filter(id=recipient_id).first()
            elif recipient_type == 'student':
                recipient = StudentExtra.objects.filter(id=recipient_id).first()
            
            if recipient:
                # Create a new message object
                message = Message(
                    sender=request.user,
                    recipient=recipient,
                    body=form.cleaned_data['body']
                )
                # Save the message to the database
                message.save()
                # Redirect to the same page to refresh and display new messages
                return redirect('admin_messaging')
    else:
        form = MessageForm()
    
    return render(request, 'college/admin_messaging.html', {'form': form, 'messages': all_messages})



@login_required(login_url='studentlogin')
def student_see_grades(request):
    # Filter grades based on the currently logged-in student's name or ID
    grades = Grade.objects.filter(student_name=request.user.studentextra.id)
    
    form = GradeForm()
    return render(request, 'college/student_see_grades.html', {'form': form, 'grades': grades})

    
def student_timetable(request):
    
    uploaded_images = UploadedImage.objects.all()
    return render(request, 'college/student_timetable.html', {'uploaded_images': uploaded_images})


def teacher_timetable(request):
   
    uploaded_images = UploadedImage.objects.all()
    return render(request, 'college/teacher_timetable.html', {'uploaded_images': uploaded_images})