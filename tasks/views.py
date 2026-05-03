from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question,StudentAnswer,StudentQuizAttempt
from .forms import QuizForm, QuestionForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Q
# Create your views here.


User=get_user_model()

@login_required
@require_POST
def change_user_role(request, user_id):

    user = get_object_or_404(User, id=user_id)

    new_role = request.POST.get("role")

    if new_role in ["admin", "teacher", "student"]:
        user.role = new_role
        user.save()

    return redirect("admin_user_list")

@login_required
def admin_user_list(request):

    users = User.objects.all().order_by("-date_joined")

    context = {
        "users": users
    }

    return render(
        request,
        "admin/user_list.html",
        context
    )
    
@login_required
def teacher_quiz_list(request):

    quizzes = Quiz.objects.filter(
        teacher=request.user
    ).order_by("-created_at")

    context = {
        "quizzes": quizzes
    }

    return render(
        request,
        "teacher/quiz_list.html",
        context
    )

@login_required
def teacher_quiz_results(request, quiz_id):

    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        teacher=request.user  # security check
    )

    attempts = StudentQuizAttempt.objects.filter(
        quiz=quiz,
        is_submitted=True
    ).select_related("student").order_by("-score")

    context = {
        "quiz": quiz,
        "attempts": attempts
    }

    return render(
        request,
        "teacher/quiz_results.html",
        context
    )


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(teacher=request.user)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_create(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.teacher = request.user
            quiz.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()

    return render(request, 'quiz/quiz_form.html', {'form': form})


@login_required
def quiz_update(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, teacher=request.user)

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'quiz/quiz_form.html', {'form': form})


@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect('quiz_list')


@login_required
def toggle_quiz_status(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.is_active = not quiz.is_active
    quiz.save()
    if request.user.is_superuser:
        return redirect("admin_quiz_list")
    else:
        return redirect("quiz_list")

def admin_quiz_list(request):

    quizzes = Quiz.objects.all().order_by("-created_at")

    
    status = request.GET.get("status")
    if status == "active":
        quizzes = quizzes.filter(is_active=True)
    elif status == "inactive":
        quizzes = quizzes.filter(is_active=False)

    
    date = request.GET.get("date")
    if date:
        quizzes = quizzes.filter(created_at__date=date)

    context = {
        "quizzes": quizzes,
    }

    return render(request,"admin/quiz_list.html",context)


@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, teacher=request.user)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_question',quiz_id=quiz.id)
    else:
        form = QuestionForm()
    questions=quiz.questions.all()
    return render(request, 'quiz/question_form.html', {
        'form': form,
        'quiz': quiz,
        'questions':questions
    })


@login_required
def question_update(request, question_id):
    question = get_object_or_404(
        Question,
        id=question_id,
        quiz__teacher=request.user
    )

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('add_question',quiz_id=question_id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'quiz/question_form.html', {'form': form})


@login_required
def question_delete(request, question_id):
    question = get_object_or_404(
        Question,
        id=question_id,
        quiz__teacher=request.user
    )
    question.delete()
    return redirect('quiz_list')


@login_required
def student_quiz_list(request):
    now = timezone.now()

    quizzes = Quiz.objects.all()
   

    return render(request, "student/quiz_list.html", {
        "quizzes": quizzes,
        "now":now 
        
    })
    
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    attempt, created = StudentQuizAttempt.objects.get_or_create(
        student=request.user,
        quiz=quiz
    )

    if attempt.is_submitted:
        return redirect("student_result", quiz.id)

    questions = quiz.questions.all()

    request.session[f"quiz_{quiz.id}_start"] = timezone.now().isoformat()

    return render(request, "student/start_quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "duration": quiz.duration
    })



@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method != "POST":
        return redirect("student_dashboard")

    # get student attempt
    attempt, created = StudentQuizAttempt.objects.get_or_create(
        student=request.user,
        quiz=quiz
    )

    
    # if attempt.is_submitted:
    #     return redirect("student_result", quiz.id)

   
    start_time_str = request.session.get(f"quiz_{quiz.id}_start")

    if start_time_str:
        start_time = timezone.datetime.fromisoformat(start_time_str)

        
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)

        end_time = start_time + timedelta(minutes=quiz.duration)

        if timezone.now() > end_time:
            print("⏰ Time exceeded! Auto-submitting...")

    questions = quiz.questions.all()
    score = 0

    for question in questions:
        selected = request.POST.get(str(question.id))

        print(
            "Question:",
            question.id,
            "Selected:",
            selected,
            "Correct:",
            question.correct_answer
        )

        if selected:
            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected
            )

            if selected == question.correct_answer:
                score += question.marks

    attempt.score = score
    attempt.is_submitted = True
    attempt.save()

   
    if f"quiz_{quiz.id}_start" in request.session:
        del request.session[f"quiz_{quiz.id}_start"]

    return redirect("student_result", quiz.id)

@login_required
def student_result(request, quiz_id):
    attempt = get_object_or_404(
        StudentQuizAttempt,
        quiz_id=quiz_id,
        student=request.user
    )

    total = attempt.quiz.total_marks
    score = attempt.score

    percentage = 0
    if total > 0:
        percentage = (score / total) * 100

    return render(request, "student/result.html", {
        "attempt": attempt,
        "percentage": round(percentage, 2)
    })

@login_required
def student_results(request):
    results = StudentQuizAttempt.objects.filter(
        student=request.user
    ).select_related("quiz").order_by("-submitted_at")

    context = {
        "results": results
    }
    return render(
        request,
        "student/student_results.html",
        context
    )
