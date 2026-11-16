from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date')
    search_fields = ('title', 'note', 'user__username')
    list_filter = ('date',)
