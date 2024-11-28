from django.shortcuts import render

from books.models import AdminBook


def home_page(request):
    monthly_books = AdminBook.get_monthly_books()
    context = {'monthly_books': monthly_books}

    return render(request, 'common/index.html', context)


