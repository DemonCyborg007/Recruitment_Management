from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('facilitator/dashboard/', views.facilitator_dashboard, name='facilitator_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/create_facilitator/', views.create_facilitator, name='create_facilitator'),
    path('facilitator/create_student/', views.create_student, name='create_student'),
    path('facilitator/create_placement_drive/', views.create_placement_drive, name='create_placement_drive'),
    path('logout/', views.logout_view , name='logout'),
    path('bulk_upload/', views.bulk_upload_students, name='bulk_upload_students'),
    path('apply_to_drive/<int:drive_id>/', views.apply_to_placement_drive, name='apply_to_placement_drive'),
    path('history/', views.student_application_history, name='student_application_history'),
    path('view_student_applications/<int:student_id>/', views.view_student_applications, name='view_student_applications'),
    path('student/update_profile/', views.update_student_profile, name='update_student_profile'),
]
