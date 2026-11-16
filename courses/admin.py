from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'description', 'content')  # Add 'content' to list_display if you want to see it in the list view
    search_fields = ('title', 'description', 'content')  # Make 'content' searchable
    list_filter = ('date',)  # Optional: filter courses by date
    ordering = ('-date',)  # Optional: order courses by date, most recent first