from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
import json


class AttendanceGroup(models.Model):
    """
    Defines which days employees are allowed to clock in.
    
    Days are stored as a list of integers:
    0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 
    4 = Friday, 5 = Saturday, 6 = Sunday
    """
    
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Group Name'
    )
    
    allowed_days = models.JSONField(
        default=list,
        verbose_name='Allowed Days',
        help_text='Days of week when employees can clock in (0=Mon, 6=Sun)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Attendance Group'
        verbose_name_plural = 'Attendance Groups'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_allowed_days_display()})"
    
    def get_allowed_days_display(self):
        """Return human-readable list of allowed days"""
        day_names = dict(self.WEEKDAYS)
        return ', '.join([day_names[day] for day in sorted(self.allowed_days)])
    
    def clean(self):
        """Validate that allowed_days contains valid integers (0-6)"""
        if not isinstance(self.allowed_days, list):
            raise ValidationError('Allowed days must be a list.')
        
        for day in self.allowed_days:
            if not isinstance(day, int) or day < 0 or day > 6:
                raise ValidationError(f'Invalid day: {day}. Must be integer between 0-6.')
    
    def is_day_allowed(self, date):
        """Check if a given date is allowed for this group"""
        return date.weekday() in self.allowed_days


class UserGroup(models.Model):
    """
    Many-to-Many relationship between Users and AttendanceGroups.
    A user can belong to multiple groups.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_groups'
    )
    
    group = models.ForeignKey(
        AttendanceGroup,
        on_delete=models.CASCADE,
        related_name='group_users'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Group Assignment'
        verbose_name_plural = 'User Group Assignments'
        unique_together = ['user', 'group']
        ordering = ['user__username', 'group__name']
    
    def __str__(self):
        return f"{self.user.username} → {self.group.name}"


class AttendanceLog(models.Model):
    """
    Records clock in/out times for employees.
    
    Business Rules:
    - One entry per day per user
    - Must have check_in before check_out
    - Can only clock in on allowed days (based on user's groups)
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendance_logs'
    )
    
    date = models.DateField(
        verbose_name='Date',
        db_index=True
    )
    
    check_in = models.TimeField(
        verbose_name='Check In Time',
        null=True,
        blank=True
    )
    
    check_out = models.TimeField(
        verbose_name='Check Out Time',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Attendance Log'
        verbose_name_plural = 'Attendance Logs'
        unique_together = ['user', 'date']
        ordering = ['-date', 'user__username']
        indexes = [
            models.Index(fields=['date', 'user']),
            models.Index(fields=['-date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def clean(self):
        """Validate attendance log"""
        # Check that check_out is not before check_in
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError('Check out time must be after check in time.')
    
    def get_total_hours(self):
        """Calculate total hours worked"""
        if self.check_in and self.check_out:
            from datetime import datetime, timedelta
            
            # Create datetime objects for today with the times
            check_in_dt = datetime.combine(self.date, self.check_in)
            check_out_dt = datetime.combine(self.date, self.check_out)
            
            # Calculate difference
            delta = check_out_dt - check_in_dt
            
            # Return hours as float
            return delta.total_seconds() / 3600
        return 0
    
    def get_total_hours_display(self):
        """Return formatted hours (e.g., '8.5 hrs')"""
        hours = self.get_total_hours()
        return f"{hours:.2f} hrs" if hours > 0 else "N/A"
    
    def is_complete(self):
        """Check if both check in and check out are recorded"""
        return self.check_in is not None and self.check_out is not None
    
    def is_active(self):
        """Check if user is currently clocked in"""
        return self.check_in is not None and self.check_out is None
