
from users.forms import CustomRegisterForm,LoginForm
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Avg
from tasks.models import StudentQuizAttempt,Quiz

User=get_user_model()
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm, CustomPasswordChangeForm



@login_required
def profile(request):

    return render(
        request,
        "accounts/profile.html",
        {"user": request.user}
    )



@login_required
def edit_profile(request):

    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,  
            instance=request.user
        )

        if form.is_valid():
            form.save()
            print(request.user.profile_image.url)
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form}
    )



@login_required
def change_password(request):

    if request.method == "POST":
        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

           
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully!")
            return redirect("profile")

    else:
        form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        "accounts/change_password.html",
        {"form": form}
    )
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

def activate_user(request, user_id, token):
    print("Incoming user_id:", user_id)
    try:
        user = User.objects.get(id=user_id)

        if user.is_active:
            messages.info(request, "Account already activated.")
            return redirect('sign_in')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully!")
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid or expired link')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
def sign_up(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)

             
            user.save()

            messages.success(request, 'Check your email to activate your account')
            return redirect('sign_in')
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/register.html', {"form": form})

    
def sign_in(request):
    
    if request.method=="POST":
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if is_admin(user):
                return redirect('admin_dashboard')
            elif is_teacher(user):
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
            
    else:
        form=LoginForm()
    return render(request,'registration/login.html',{"form":form})
        
    
def logout_view(request):
    if request.method=="POST":
        logout(request)
    
        return redirect('sign_in')
@user_passes_test(is_admin,login_url='no_permission')
def admin_dashboard(request):
    total_users = User.objects.count()

   
    total_quiz = Quiz.objects.all().count()

    
    total_inactive_quiz = Quiz.objects.filter(
        is_active=False
    ).count()

    total_attempted_students = StudentQuizAttempt.objects.filter(
        is_submitted=True
    ).values("student").distinct().count()

    context = {
        "total_users": total_users,
        "total_quiz": total_quiz,
        "total_inactive_quiz": total_inactive_quiz,
        "total_attempted_students": total_attempted_students,
    }

    return render(request,'admin/dashboard_body.html',context)

@user_passes_test(is_student,login_url='no_permission')
def student_dashboard(request):
    active_quizzes = Quiz.objects.filter(
        is_active=True,
        start_time__lte=timezone.now()
    )
    total_quizzes = Quiz.objects.all().count()

    total_active = active_quizzes.count()

    
    attempts = StudentQuizAttempt.objects.filter(
        student=request.user,
        is_submitted=True
    )

    total_attempted = attempts.count()

   
    best_score = attempts.aggregate(Max("score"))["score__max"]

    

    context = {
        "total_quizzes":total_quizzes,
        "total_active": total_active,
        "total_attempted": total_attempted,
        "best_score": best_score or 0,
        
    }
    return render(request,'student/dashboard_body.html',context)
@user_passes_test(is_teacher,login_url='no_permission')
def teacher_dashboard(request):
        total_quiz = Quiz.objects.filter(
                teacher=request.user
            ).count()

        # 2️⃣ Total active quizzes of this teacher
        total_active = Quiz.objects.filter(
            teacher=request.user,
            is_active=True
        ).count()

            # 3️⃣ Total unique students who attempted teacher quizzes
        total_students = StudentQuizAttempt.objects.filter(
            quiz__teacher=request.user,
            is_submitted=True
        ).values("student").distinct().count()

        context = {
            "total_quiz": total_quiz,
            "total_active": total_active,
            "total_students": total_students,
        }


        return render(request,'teacher/dashboard_body.html',context)