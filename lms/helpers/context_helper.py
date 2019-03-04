import os
from lms import models
from django.conf import settings


def course_helper():
    courses = models.Course.objects.filter(soft_delete=False)
    return {i.pk: i.name for i in courses}

def subject_helper():
    subject = models.Subject.objects.filter(soft_delete=False)
    return {i.pk: i.name for i in subject}

def gender_helper():
    gender_type =[
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    return gender_type

def get_user_info(user):
    genders = gender_helper()
    info = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'mobile': user.mobile,
        'email': user.email,
        'dob': user.dob,
        'address': user.address,
        'is_student': user.is_student,
        'is_employee': user.is_employee,
        'photo': os.path.join(settings.MEDIA_URL, user.photo.name) if user.photo else None,
    }
    return info
