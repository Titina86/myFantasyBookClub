from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, View, DetailView

from books.models import MyBook
from booksList.forms import BooksListAddForm, EditBookForm

from booksList.models import BooksList


class MyBookListView(LoginRequiredMixin, ListView):
    model = BooksList
    template_name = 'books/my-list-books.html'
    context_object_name = 'books'


class AddBookView(LoginRequiredMixin, FormView):
    form_class = BooksListAddForm
    template_name = 'books/my-book-add.html'

    def form_valid(self, form):
        # Ensure the profile is passed from the logged-in user
        form.save(profile=self.request.user.profile)

        # After saving, redirect to the user's book list or another page
        return redirect('my-books')

    def form_invalid(self, form):
        # If the form is invalid, re-render the form with errors
        return render(self.request, self.template_name, {'form': form})


class EditBookView(LoginRequiredMixin, View):
    template_name = 'books/my-book-edit.html'

    def get(self, request, pk):
        # Get the book entry that belongs to the logged-in user
        book = get_object_or_404(MyBook, pk=pk)
        books_list_entry = get_object_or_404(BooksList, profile=request.user.profile, book=book)

        # Instantiate the form with existing book data
        form = EditBookForm(book=book, profile=request.user.profile)
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(MyBook, pk=pk)
        books_list_entry = get_object_or_404(BooksList, profile=request.user.profile, book=book)

        form = EditBookForm(request.POST, book=book, profile=request.user.profile)

        if form.is_valid():
            # Save the form data (update MyBook and BooksList models)
            form.save()
            return redirect('my-books')  # Redirect after successful form submission

        # If form is invalid, re-render the page with the errors
        return render(request, self.template_name, {'form': form, 'book': book})


def detail_book(request, pk):
    book = MyBook.objects.get(pk=pk)
    profile = request.user.profile
    book_list_entry = BooksList.objects.get(book=book, profile=profile)

    context = {
        'book': book,
        'book_list_entry': book_list_entry,
        'profile': profile
    }

    return render(request, 'books/my-book-details.html', context)


class DeleteBookFromListView(View):
    def get(self, request, *args, **kwargs):
        # Получаваме BooksList обекта по неговия `pk` и профил на потребителя
        book_entry = BooksList.objects.get(book_id=kwargs['pk'], profile=request.user.profile)

        # Предаваме книгата на шаблона, за да я показваме за потвърждение
        return render(request, 'books/my-book-delete.html', {'book': book_entry})

    def post(self, request, *args, **kwargs):
        # Изтриваме BooksList обекта от базата
        book_entry = BooksList.objects.get(book_id=kwargs['pk'], profile=request.user.profile)
        book_entry.delete()

        messages.success(request, 'Книгата беше успешно премахната от списъка ви.')
        # Връщане към същия шаблон след изтриването
        return redirect('my-books')


def wish_list_view(request):
    # Получаваме списъка с книги с статус 'wish_list' за текущия потребител
    wish_list_books = BooksList.objects.filter(profile=request.user.profile, read_status=BooksList.ReadStatus.WISH_LIST)

    # Предаваме списъка на шаблона
    return render(request, 'books/wish-list.html', {'wish_list_books': wish_list_books})