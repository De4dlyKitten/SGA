from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from attendance.models import AttendanceGroup, UserGroup

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting database seed...'))
        
        # Create Super Admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@sga-lite.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: admin / admin123'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('! Admin user already exists'))
        
        # Create sample employee
        if not User.objects.filter(username='employee1').exists():
            employee1 = User.objects.create_user(
                username='employee1',
                email='employee1@sga-lite.com',
                password='password123',
                first_name='John',
                last_name='Doe',
                role='EMPLOYEE'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created employee: employee1 / password123'))
        else:
            employee1 = User.objects.get(username='employee1')
            self.stdout.write(self.style.WARNING('! Employee1 already exists'))
        
        # Create Attendance Groups
        weekday_group, created = AttendanceGroup.objects.get_or_create(
            name='Weekday Shift',
            defaults={'allowed_days': [0, 1, 2, 3, 4]}  # Mon-Fri
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created group: Weekday Shift (Mon-Fri)'))
        else:
            self.stdout.write(self.style.WARNING('! Weekday Shift group already exists'))
        
        weekend_group, created = AttendanceGroup.objects.get_or_create(
            name='Weekend Shift',
            defaults={'allowed_days': [5, 6]}  # Sat-Sun
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created group: Weekend Shift (Sat-Sun)'))
        else:
            self.stdout.write(self.style.WARNING('! Weekend Shift group already exists'))
        
        fulltime_group, created = AttendanceGroup.objects.get_or_create(
            name='Full Time',
            defaults={'allowed_days': [0, 1, 2, 3, 4, 5, 6]}  # All days
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created group: Full Time (All days)'))
        else:
            self.stdout.write(self.style.WARNING('! Full Time group already exists'))
        
        # Assign employee to weekday group
        UserGroup.objects.get_or_create(
            user=employee1,
            group=weekday_group
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Assigned employee1 to Weekday Shift'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Database seeded successfully! ==='))
        self.stdout.write(self.style.SUCCESS('\nYou can now login with:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Employee: employee1 / password123'))
