Smart Quiz Management System

A modern web-based Quiz Management System built with Django that enables students, teachers, and admins to manage and participate in online quizzes efficiently.

🚀 Project Overview

Smart Quiz is an online examination platform where:

👨‍🏫 Teachers can create and manage quizzes
👨‍🎓 Students can attend quizzes with a timer
🛡️ Admin can manage users and monitor the system
📊 Students can view quiz results instantly

The system includes authentication, profile management, role-based dashboards, quiz timers, scoring, and result tracking.

✨ Features
🔐 Authentication System
User Registration
Login & Logout
Forgot Password
Reset Password
Change Password
Role-based Authentication
👤 User Roles
👨‍🎓 Student
View available quizzes
Start quizzes
Timed quiz system
Auto-submit on timeout
View results and scores
Edit profile
👨‍🏫 Teacher
Create quizzes
Update/Delete quizzes
Add questions
Manage quiz status
View created quizzes
🛡️ Admin
Manage all users
Manage quizzes
Access admin dashboard
🧠 Quiz Features
Timed quizzes
Auto-submit functionality
MCQ-based questions
Marks calculation
Result history
Score percentage
Quiz availability based on start time
🎨 UI/UX Features
Modern dashboard design
Responsive layout
Animated forms
Professional profile page
Custom authentication pages
Stylish navbar
Interactive quiz interface
🛠️ Technologies Used
Technology	Purpose
Django	Backend Framework
Python	Programming Language
PostgreSQL	Database
HTML5	Structure
Tailwind CSS	Styling
JavaScript	Timer & Interactions
Django Template Language	Frontend Rendering
📂 Project Structure
quiz_management/
│
├── accounts/        # Authentication & user management
├── tasks/           # Quiz & question management
├── dashboard/       # Dashboards
├── media/           # Uploaded profile images
├── static/          # Static files
├── templates/       # HTML templates
├── quiz_management/ # Main project settings
│
├── manage.py
└── requirements.txt

🧩 OOP Concepts Used

This project follows Object-Oriented Programming principles using Django.

✅ Inheritance
class CustomUser(AbstractUser):
CustomUser inherits from Django's AbstractUser

✅ Encapsulation
Models encapsulate related data and behaviors

Example:

class Quiz(models.Model):

✅ Abstraction
Django Forms abstract validation and rendering logic

Example:

class QuizForm(forms.ModelForm):

✅ Reusability
StyledFormMixin used for reusable form styling

Example:

class QuizForm(StyledFormMixin, forms.ModelForm):
📸 Screenshots
Authentication
Login Page
Signup Page
Forgot Password
Dashboards
Student Dashboard
Teacher Dashboard
Admin Dashboard
Quiz System
Quiz Attempt Page
Timer Interface
Result Page



⚙️ ###Installation Guide

1️⃣ ####Clone Repository
git clone https://github.com/your-username/smart-quiz.git

2️⃣ ####Create Virtual Environment
python -m venv venv

Activate:

Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate

3️⃣ ####Install Dependencies
pip install -r requirements.txt

4️⃣ ####Run Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ ####Create Superuser
python manage.py createsuperuser

6️⃣ ####Run Server
python manage.py runserver
🔑 Default Roles
Role	Access
Student	Attend quizzes
Teacher	Manage quizzes
Admin	Full system control
📈 Future Improvements
Live leaderboard
Email notifications
Certificate generation
Dark mode
AI-based quiz generation
Question categories
Analytics dashboard
🎯 Learning Outcomes

Through this project, I learned:

Django Authentication
Role-based Authorization
CRUD Operations
File Upload Handling
Form Validation
Session Management
Timer Logic with JavaScript
Responsive UI Design
OOP Concepts in Django
🤝 Contributing

Contributions are welcome.

Fork the repository and create a pull request.

📧 Contact
Developer

Md Zuel

LinkedIn: https://www.linkedin.com/in/md-zuel-rana-21004a26a/
GitHub: https://github.com/mdzuelrana
