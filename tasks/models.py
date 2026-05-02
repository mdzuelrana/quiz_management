from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
User = settings.AUTH_USER_MODEL


class Quiz(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    start_time = models.DateTimeField(
        help_text="Quiz start date & time",null=True,blank=True
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    total_marks = models.PositiveIntegerField()

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def end_time(self):
        if not self.start_time:
            return None
        return self.start_time + timedelta(minutes=self.duration)

    def is_running(self):
        if not self.start_time:
            return False
        now = timezone.now()
        return (
            self.is_active and
            self.start_time <= now <= self.end_time()
        )

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    CORRECT_CHOICES = (
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    )
    correct_answer = models.CharField(
        max_length=1,
        choices=CORRECT_CHOICES
    )

    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text[:50]


class StudentQuizAttempt(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_attempts"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts"
    )
    score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "quiz")

    def __str__(self):
        return f"{self.student} - {self.quiz}"
    

class StudentAnswer(models.Model):
    attempt = models.ForeignKey(
        StudentQuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    selected_option = models.CharField(max_length=1)

    def is_correct(self):
        return self.selected_option == self.question.correct_answer
