
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from .models import Book, Student, Issue


# =====================================
# ADMIN CHECK
# =====================================

def is_admin(user):
    return user.is_authenticated and user.is_staff


# =====================================
# ADMIN DASHBOARD
# =====================================

@user_passes_test(is_admin)
def home(request):

    total_books = Book.objects.count()
    total_students = Student.objects.count()

    issued_books = Issue.objects.filter(
        return_date__isnull=True
    ).count()

    returned_books = Issue.objects.filter(
        return_date__isnull=False
    ).count()

    total_fine = sum(
        issue.calculate_fine()
        for issue in Issue.objects.all()
    )

    context = {
        'total_books': total_books,
        'total_students': total_students,
        'issued_books': issued_books,
        'returned_books': returned_books,
        'total_fine': total_fine,
    }

    return render(request, 'home.html', context)


# =====================================
# BOOK LIST AND SEARCH
# =====================================

@user_passes_test(is_admin)
def book_list(request):

    query = request.GET.get('search', '')

    books = Book.objects.all()

    if query:
        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        )

    context = {
        'books': books,
        'query': query,
    }

    return render(request, 'book_list.html', context)


# =====================================
# ADD BOOK
# =====================================

@user_passes_test(is_admin)
def add_book(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        quantity = request.POST.get('quantity')

        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity
        )

        messages.success(request, 'Book added successfully!')

        return redirect('book_list')

    return render(request, 'add_book.html')


# =====================================
# EDIT BOOK
# =====================================

@user_passes_test(is_admin)
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':

        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.quantity = request.POST.get('quantity')

        book.save()

        messages.success(request, 'Book updated successfully!')

        return redirect('book_list')

    return render(
        request,
        'edit_book.html',
        {'book': book}
    )


# =====================================
# DELETE BOOK
# =====================================

@user_passes_test(is_admin)
def delete_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':

        book.delete()

        messages.success(request, 'Book deleted successfully!')

        return redirect('book_list')

    return render(
        request,
        'delete_book.html',
        {'book': book}
    )


# =====================================
# STUDENT LIST
# =====================================

@user_passes_test(is_admin)
def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        'student_list.html',
        {'students': students}
    )


# =====================================
# ADD STUDENT
# =====================================

@user_passes_test(is_admin)
def add_student(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        Student.objects.create(
            name=name,
            student_id=student_id,
            department=department,
            phone=phone
        )

        messages.success(request, 'Student added successfully!')

        return redirect('student_list')

    return render(request, 'add_student.html')


# =====================================
# EDIT STUDENT
# =====================================

@user_passes_test(is_admin)
def edit_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':

        student.name = request.POST.get('name')
        student.student_id = request.POST.get('student_id')
        student.department = request.POST.get('department')
        student.phone = request.POST.get('phone')

        student.save()

        messages.success(request, 'Student updated successfully!')

        return redirect('student_list')

    return render(
        request,
        'edit_student.html',
        {'student': student}
    )


# =====================================
# DELETE STUDENT
# =====================================

@user_passes_test(is_admin)
def delete_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':

        student.delete()

        messages.success(request, 'Student deleted successfully!')

        return redirect('student_list')

    return render(
        request,
        'delete_student.html',
        {'student': student}
    )


# =====================================
# ISSUE BOOK
# =====================================

@user_passes_test(is_admin)
def issue_book(request):

    students = Student.objects.all()
    books = Book.objects.filter(quantity__gt=0)

    if request.method == 'POST':

        student_id = request.POST.get('student')
        book_id = request.POST.get('book')

        student = get_object_or_404(Student, id=student_id)
        book = get_object_or_404(Book, id=book_id)

        if book.quantity > 0:

            Issue.objects.create(
                student=student,
                book=book
            )

            book.quantity -= 1
            book.save()

            messages.success(request, 'Book issued successfully!')

            return redirect('issue_list')

        messages.error(request, 'Book is not available!')

    context = {
        'students': students,
        'books': books,
    }

    return render(request, 'issue_book.html', context)


# =====================================
# ISSUE LIST
# =====================================

@user_passes_test(is_admin)
def issue_list(request):

    issues = Issue.objects.all().order_by('-issue_date')

    return render(
        request,
        'issue_list.html',
        {'issues': issues}
    )


# =====================================
# RETURN BOOK
# =====================================

@user_passes_test(is_admin)
def return_book(request, issue_id):

    issue = get_object_or_404(
        Issue,
        id=issue_id,
        return_date__isnull=True
    )

    if request.method == 'POST':

        issue.return_date = timezone.now().date()
        issue.save()

        issue.book.quantity += 1
        issue.book.save()

        messages.success(request, 'Book returned successfully!')

        return redirect('issue_list')

    return render(
        request,
        'return_book.html',
        {'issue': issue}
    )


# =====================================
# STUDENT REGISTRATION
# =====================================

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        student_id = request.POST.get('student_id')

        if form.is_valid():

            try:

                student = Student.objects.get(
                    student_id=student_id,
                    user__isnull=True
                )

                user = form.save()

                student.user = user
                student.save()

                messages.success(
                    request,
                    'Account created successfully!'
                )

                return redirect('login')

            except Student.DoesNotExist:

                messages.error(
                    request,
                    'Invalid Student ID or account already linked.'
                )

    else:

        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )


# =====================================
# STUDENT DASHBOARD
# =====================================

@login_required
def user_dashboard(request):

    query = request.GET.get('search', '')

    books = Book.objects.all().order_by('title')

    if query:

        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        )

    student = Student.objects.filter(
        user=request.user
    ).first()

    if student:

        issues = Issue.objects.filter(
            student=student
        ).order_by('-issue_date')

    else:

        issues = []

    total_fine = sum(
        issue.calculate_fine()
        for issue in issues
    )

    context = {
        'books': books,
        'student': student,
        'issues': issues,
        'query': query,
        'total_fine': total_fine,
    }

    return render(
        request,
        'user_dashboard.html',
        context
    )


# =====================================
# CUSTOM LOGIN
# =====================================

class CustomLoginView(LoginView):

    def get_success_url(self):

        if self.request.user.is_superuser or self.request.user.is_staff:
            return '/'

        return '/user-dashboard/'

# =====================================
# FINE REPORT
# =====================================



# =====================================
# FINE REPORT
# =====================================

@user_passes_test(is_admin)
def fine_report(request):

    issues = Issue.objects.all().order_by('-issue_date')

    fine_issues = [
        issue for issue in issues
        if issue.calculate_fine() > 0
    ]

    for issue in fine_issues:

        end_date = issue.return_date or timezone.now().date()

        due_date = issue.issue_date + timedelta(days=14)

        issue.late_days = max(
            (end_date - due_date).days,
            0
        )

    total_fine = sum(
        issue.calculate_fine()
        for issue in fine_issues
    )

    return render(
        request,
        'fine_report.html',
        {
            'issues': fine_issues,
            'total_fine': total_fine,
        }
    )


# =====================================
# FINE PAYMENT
# =====================================

@user_passes_test(is_admin)
def fine_payment(request):

    if request.method == 'POST':

        issue_id = request.POST.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id)

        if issue.fine_paid:
            messages.warning(request, 'Fine already paid!')

        elif issue.calculate_fine() <= 0:
            messages.error(request, 'No fine is due for this book!')

        else:
            issue.fine_paid = True
            issue.fine_paid_date = timezone.now().date()
            issue.save()

            messages.success(request, 'Fine payment successful!')

        return redirect('fine_payment')

    issues = Issue.objects.all().order_by('-issue_date')

    fine_issues = []

    for issue in issues:
        issue.fine_amount = issue.calculate_fine()

        if issue.fine_amount > 0:
            fine_issues.append(issue)

    total_fine = sum(
        issue.fine_amount for issue in fine_issues
    )

    total_paid = sum(
        issue.fine_amount
        for issue in fine_issues
        if issue.fine_paid
    )

    total_due = total_fine - total_paid

    context = {
        'issues': fine_issues,
        'total_fine': total_fine,
        'total_paid': total_paid,
        'total_due': total_due,
    }

    return render(request, 'fine_payment.html', context)

    
