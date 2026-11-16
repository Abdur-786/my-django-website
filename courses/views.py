from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course


def course_overview(request):
    courses = Course.objects.all().order_by('date', 'title')
    return render(request, 'courses/course_overview.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != 'POST':
        return redirect('courses:course_detail', course_id=course.id)

    course.users_enrolled.add(request.user)
    messages.success(request, f'You are enrolled in {course.title}.')
    return redirect('users:profile')
