from datetime import date

from django.contrib import admin
from django.core.exceptions import ValidationError

from books.models import AdminBook


# class AdminBookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'is_monthly_book', 'monthly_book_date')
#     list_filter = ('is_monthly_book', 'monthly_book_date')
#     actions = ['set_monthly_books']
#
#     def save_model(self, request, obj, form, change):
#         if obj.is_monthly_book:
#             current_month_books = AdminBook.objects.filter(
#                 is_monthly_book=True,
#                 monthly_book_date__month=date.today().month,
#                 monthly_book_date__year=date.today().year
#             )
#             if current_month_books.count() >= 3:
#                 raise ValueError("Only 3 monthly books are allowed per month.")
#         super().save_model(request, obj, form, change)
#
@admin.register(AdminBook)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_monthly_book', 'monthly_book_date')

    list_filter = ('is_monthly_book', 'monthly_book_date')
    actions = ['set_monthly_books']

    def save_model(self, request, obj, form, change):
        if obj.is_monthly_book:
            current_month_books = AdminBook.objects.filter(
                is_monthly_book=True,
                monthly_book_date__month=date.today().month,
                monthly_book_date__year=date.today().year
            )
            if current_month_books.count() >= 3:
                raise ValidationError("Only 3 monthly books are allowed per month.")
        super().save_model(request, obj, form, change)