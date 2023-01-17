from django.contrib.auth.backends import BaseBackend
from .models import Student

class StudentBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            student = Student.objects.get(email=email)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
