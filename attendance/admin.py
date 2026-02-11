from django.contrib import admin
from django.utils.html import format_html
from .models import AttendanceGroup, UserGroup, AttendanceLog


@admin.register(AttendanceGroup)
class AttendanceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_allowed_days', 'user_count', 'created_at')
    search_fields = ('name',)
    
    def display_allowed_days(self, obj):
        return obj.get_allowed_days_display()
    display_allowed_days.short_description = 'Allowed Days'
    
    def user_count(self, obj):
        count = obj.group_users.count()
        return format_html('<strong>{}</strong> users', count)
    user_count.short_description = 'Users'


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'assigned_at')
    list_filter = ('group', 'assigned_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'group__name')
    autocomplete_fields = ['user', 'group']


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in', 'check_out', 'display_total_hours', 'display_status')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at', 'get_total_hours_display')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'date')
        }),
        ('Time Records', {
            'fields': ('check_in', 'check_out', 'get_total_hours_display')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_total_hours(self, obj):
        return obj.get_total_hours_display()
    display_total_hours.short_description = 'Total Hours'
    
    def display_status(self, obj):
        if obj.is_complete():
            return format_html('<span style="color: green;">✓ Complete</span>')
        elif obj.is_active():
            return format_html('<span style="color: orange;">⏱ Active</span>')
        else:
            return format_html('<span style="color: gray;">○ Pending</span>')
    display_status.short_description = 'Status'
