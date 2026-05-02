from django.urls import path
from tasks import views

urlpatterns = [
    path('quiz/list', views.quiz_list, name='quiz_list'),
    path('create/', views.quiz_create, name='quiz_create'),
    path('update/<int:quiz_id>/', views.quiz_update, name='quiz_update'),
    path('delete/<int:quiz_id>/', views.quiz_delete, name='quiz_delete'),
    path('toggle/<int:quiz_id>/', views.toggle_quiz_status, name='quiz_toggle'),

    path('<int:quiz_id>/question/add/', views.add_question, name='add_question'),
    path('question/update/<int:question_id>/', views.question_update, name='question_update'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path("teacher/results/",views.teacher_quiz_list,name="teacher_quiz_list"),
    path("teacher/results/<int:quiz_id>/",views.teacher_quiz_results,name="teacher_quiz_results"),
    
    path("student/quizzes/", views.student_quiz_list, name="student_quiz_list"),
    path("student/quiz/<int:quiz_id>/start/", views.start_quiz, name="start_quiz"),
    path("student/quiz/<int:quiz_id>/result/", views.student_result, name="student_result"),
    path("student/results/",views.student_results,name="student_results"),
    
    path("admin/quizzes/",views.admin_quiz_list,name="admin_quiz_list"),
    path("admin/users/",views.admin_user_list,name="admin_user_list"),
    path("admin/users/change-role/<int:user_id>/",views.change_user_role,name="change_user_role"),




]
