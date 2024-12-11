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
        form.save(profile=self.request.user.profile)

        return redirect('my-books')

    def form_invalid(self, form):

        return render(self.request, self.template_name, {'form': form})


class EditBookView(LoginRequiredMixin, View):
    template_name = 'books/my-book-edit.html'

    def get(self, request, pk):

        book = get_object_or_404(MyBook, pk=pk)
        books_list_entry = get_object_or_404(BooksList, profile=request.user.profile, book=book)

        form = EditBookForm(book=book, profile=request.user.profile)
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(MyBook, pk=pk)
        books_list_entry = get_object_or_404(BooksList, profile=request.user.profile, book=book)

        form = EditBookForm(request.POST, book=book, profile=request.user.profile)

        if form.is_valid():

            form.save()
            return redirect('my-books')

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

        book_entry = BooksList.objects.get(book_id=kwargs['pk'], profile=request.user.profile)

        return render(request, 'books/my-book-delete.html', {'book': book_entry})

    def post(self, request, *args, **kwargs):

        book_entry = BooksList.objects.get(book_id=kwargs['pk'], profile=request.user.profile)
        book_entry.delete()

        messages.success(request, 'The book was successfully deleted')

        return redirect('my-books')


def wish_list_view(request):

    wish_list_books = BooksList.objects.filter(profile=request.user.profile, read_status=BooksList.ReadStatus.WISH_LIST)


    return render(request, 'books/wish-list.html', {'wish_list_books': wish_list_books})