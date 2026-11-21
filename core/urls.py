
from django.urls import path
from . import views

urlpatterns = [

    # Admin Dashboard
    path('', views.home, name='home'),

    # Book Management
    path('books/', views.book_list, name='book_list'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    # Issue and Return Books
    path('issue-book/', views.issue_book, name='issue_book'),
    path('issue-list/', views.issue_list, name='issue_list'),
    path('return-book/<int:issue_id>/', views.return_book, name='return_book'),

    # Student Registration and Dashboard
    path('register/', views.register, name='register'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    # Fine Report
    path('fine-report/', views.fine_report, name='fine_report'),
    path('fine-payment/', views.fine_payment, name='fine_payment'),

]
