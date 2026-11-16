from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


@login_required
def add_note(request):
    form = NoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        messages.success(request, 'Note added successfully.')
        return redirect('notes:view_notes')

    return render(request, 'notes/add_note.html', {'form': form})


@login_required
def view_notes(request):
    date_filter = request.GET.get('date', '')
    notes = Note.objects.filter(user=request.user).order_by('-date', '-id')

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
        except ValueError:
            date_obj = None
        if date_obj:
            notes = notes.filter(date=date_obj)
        else:
            messages.error(request, 'Invalid date filter. Showing all your notes.')
            date_filter = ''

    return render(request, 'notes/view_notes.html', {
        'notes': notes,
        'date_filter': date_filter,
    })


@login_required
def delete_note(request, note_id):
    note = Note.objects.filter(id=note_id, user=request.user).first()

    if note is None:
        messages.error(request, 'That note could not be found.')
        return redirect('notes:view_notes')

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted.')

    return redirect('notes:view_notes')
