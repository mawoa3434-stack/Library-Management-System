
from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Issue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    # Fine Payment Information
    fine_paid = models.BooleanField(default=False)
    fine_paid_date = models.DateField(null=True, blank=True)

    def calculate_fine(self):
        from datetime import timedelta
        from django.utils import timezone

        end_date = self.return_date or timezone.now().date()
        due_date = self.issue_date + timedelta(days=14)

        late_days = (end_date - due_date).days

        if late_days > 0:
            return late_days * 5

        return 0

    def __str__(self):
        return f"{self.student.name} - {self.book.title}"
