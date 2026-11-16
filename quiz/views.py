from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Quiz, QuizDetail


def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('name')
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})


@login_required
def quizzes(request):
    quizzes = Quiz.objects.all().order_by('name')
    details = {
        detail.quiz_id: detail
        for detail in QuizDetail.objects.filter(user=request.user).select_related('quiz')
    }
    quiz_rows = [
        {'quiz': quiz, 'result': details.get(quiz.id)}
        for quiz in quizzes
    ]
    return render(request, 'quiz/quizzes.html', {'quiz_rows': quiz_rows})


@login_required
def quiz_form(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all().order_by('id'))

    if request.method == 'POST':
        if not questions:
            messages.error(request, 'This quiz has no questions yet.')
            return redirect('quiz:quiz_detail', quiz_id=quiz.id)

        selected_answers = {}
        invalid_questions = []

        for question in questions:
            raw_answer = request.POST.get(f'question-{question.id}')
            try:
                answer = int(raw_answer)
            except (TypeError, ValueError):
                answer = None

            if answer not in (1, 2, 3):
                invalid_questions.append(question.id)
            selected_answers[question.id] = answer

        if invalid_questions:
            messages.error(request, 'Please answer every question before submitting.')
            return render(request, 'quiz/quiz_form.html', {
                'quiz': quiz,
                'questions': questions,
            })

        correct_answers = sum(
            selected_answers[question.id] == question.correct
            for question in questions
        )
        result_percentage = round((correct_answers / len(questions)) * 100, 2)

        if result_percentage == 100:
            reward = 'gold'
        elif result_percentage >= 80:
            reward = 'silver'
        elif result_percentage >= 60:
            reward = 'bronze'
        else:
            reward = 'no reward'

        QuizDetail.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'result': result_percentage, 'reward': reward},
        )

        return redirect('quiz:result', quiz_id=quiz.id)

    return render(request, 'quiz/quiz_form.html', {
        'quiz': quiz,
        'questions': questions,
    })


@login_required
def result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_detail = QuizDetail.objects.filter(user=request.user, quiz=quiz).first()

    if quiz_detail is None:
        messages.info(request, 'Complete the quiz to see your result.')
        return redirect('quiz:quiz_form', quiz_id=quiz.id)

    return render(request, 'quiz/result.html', {
        'quiz': quiz,
        'quiz_detail': quiz_detail,
    })
