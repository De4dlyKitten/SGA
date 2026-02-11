from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Group Management
    path('groups/', views.manage_groups, name='manage_groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:user_id>/assign-groups/', views.assign_user_to_group, name='assign_user_groups'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_excel, name='export_excel'),
]
