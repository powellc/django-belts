from dojo.models import Student

def load_student(request):
    try:
        stu = Student.objects.get(user=request.user)
    except:
        stu = None
    return {'student': stu}