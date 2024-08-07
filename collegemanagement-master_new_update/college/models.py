from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# subjects=[('Discrete maths','Discrete maths'),('data structure','data structure'),('computer networks','computer networks'),('UNIX','UNIX'),('software engineering','software engineering')]
Department=[('Branch','Branch'),('ME','ME'),('CSE','CSE')]
class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    subjects = models.CharField(max_length=40)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    Department=models.CharField(max_length=10,choices=Department,default='Branch')
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name



YEAR_CHOICES = (
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
)

SEMESTER_CHOICES = (
    (1, '1st Semester'),
    (2, '2nd Semester'),
    (3, '3rd Semester'),
    (4, '4th Semester'),
    (5, '5th Semester'),
    (6, '6th Semester'),
    (7, '7th Semester'),
    (8, '8th Semester'),
    # Add more semesters as needed
)
classes=[('Branch','Branch'),('ME','ME'),('CSE','CSE')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.CharField(max_length=40,null=True)
    cl= models.CharField(max_length=10,choices=classes,default='Branch')
    status=models.BooleanField(default=False)
    year = models.IntegerField(choices=YEAR_CHOICES)
    sem = models.IntegerField(choices=SEMESTER_CHOICES)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)


# teacher-resorce add new funtion
class Resource(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class ResourceVersion(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    file = models.FileField(upload_to='resource_versions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
#  added new one foe shedule classes

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)    

class Classroom(models.Model):
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.subject} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['start_time']

# from django.db import models
# from django.contrib.auth.models import User

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional fields for the teacher

#     def __str__(self):
#         return self.user.username

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional fields for the student

#     def __str__(self):
#         return self.user.username

# class Course(models.Model):
#     name = models.CharField(max_length=100)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class Assignment(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Exam(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Project(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Grade(models.Model):
#     student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
#     assignment =models.CharField(max_length=100)
#     exam = models.CharField(max_length=100)
#     project = models.CharField(max_length=100)
#     score = models.DecimalField(max_digits=5, decimal_places=2)
  
#     def __str__(self):
#         return f"{self.student} - Grade: {self.score}"





# ye working code hai for grading system

# class Grade(models.Model):
#     student_name = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=50)
#     assignment_grade = models.DecimalField(max_digits=5, decimal_places=2)
#     exam_grade = models.DecimalField(max_digits=5, decimal_places=2)
#     project_grade = models.DecimalField(max_digits=5, decimal_places=2)

#     @property
#     def student_class(self):
#         return self.student_name.cl

#     def __str__(self):
#         return f"{self.student_name} - Grade: {self.assignment_grade}, {self.exam_grade}, {self.project_grade}"

class Grade(models.Model):
    student_name = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    assignment_grade = models.DecimalField(max_digits=5, decimal_places=2)
    exam_grade = models.DecimalField(max_digits=5, decimal_places=2)
    project_grade = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def student_class(self):
        return self.student_name.cl

    def get_grade_letter(self, score):
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B+'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C+'
        elif score >= 40:
            return 'C'
        else:
            return 'F'

    def get_grade_letter_exam(self, score):
        passing_mark = 10  # Passing mark out of 20

        if score >= 18:
            return 'A+'
        elif score >= 16:
            return 'A'
        elif score >= 14:
            return 'B+'
        elif score >= 12:
            return 'B'
        elif score >= 10:
            return 'C+'
        elif score >= 8:
            return 'C'
        elif score >= passing_mark:
            return 'D'
        else:
            return 'F'

    def get_assignment_grade_letter(self):
        return self.get_grade_letter_exam(self.assignment_grade)

    def get_exam_grade_letter(self):
        return self.get_grade_letter(self.exam_grade)

    def get_project_grade_letter(self):
        return self.get_grade_letter_exam(self.project_grade)

    def update_grades(self, assignment_grade, exam_grade, project_grade):
        self.assignment_grade = assignment_grade
        self.exam_grade = exam_grade
        self.project_grade = project_grade
        self.save()

    def __str__(self):
        return f"{self.student_name} - {self.subject}"

class Message(models.Model):
    sender = models.ForeignKey(StudentExtra, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(TeacherExtra, on_delete=models.CASCADE, related_name='received_messages')
    
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender.get_name}, To: {self.recipient.get_name},"
    
class Messageteachrs(models.Model):
    sender = models.ForeignKey(TeacherExtra, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(StudentExtra, on_delete=models.CASCADE, related_name='received_messages')
    
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender.get_name}, To: {self.recipient.get_name},"
    
    
    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    
  