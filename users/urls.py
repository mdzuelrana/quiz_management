from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import sign_in,sign_up,activate_user,logout_view,admin_dashboard,student_dashboard,teacher_dashboard,profile,edit_profile,change_password
urlpatterns = [
    path('sign_in/',sign_in,name='sign_in'),
    path('sign_up/',sign_up,name='sign_up'),
    path('logout/',logout_view,name='logout'),
    
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/password/",change_password, name="change_password"),
    
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('teacher_dashboard/',teacher_dashboard,name='teacher_dashboard'),
    path('student_dashboard/',student_dashboard,name='student_dashboard'),
    
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate_user'),
    
   


    path("password-reset/",auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="password_reset"),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),

]
