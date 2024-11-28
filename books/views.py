from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, View

from accounts.models import Profile
from .models import AdminBook


class AdminBookDetailsView(DetailView):
    model = AdminBook
    template_name = "books/admin-book-details.html"


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MyBook
from .forms import MyBookForm


class MyBookListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'books/my-list-books.html'
    context_object_name = 'profile'

    def get_queryset(self):
        # Вземаме профила на текущия потребител (self.request.user.profile)
        profile = self.request.user.profile
        return Profile.objects.filter(pk=profile.pk)  # Връща текущия профил на потребителя

    def get_context_data(self, **kwargs):
        # Добавяме към контекста свързаните книги на текущия профил
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile  # Получаваме профила на текущия потребител
        context['books'] = MyBook.objects.filter(profile=profile)  # Филтрираме книгите за този профил
        return context


    # @login_required
# def my_books(request):
#     books = MyBook.objects.filter(user=request.user)
#     return render(request, 'books/my-list-books.html', {'books': books})


class MyBookAddView(LoginRequiredMixin, View):
    template_name = 'books/my-book-add.html'

    def get(self, request):
        """Отговаря за показване на формата за добавяне на книга."""
        form = MyBookForm()
        return render(request, 'books/my-book-add.html', {'form': form})

    def post(self, request):
        """Обработва изпращането на формата."""
        profile = request.user.profile  # Вземете профила на текущия потребител
        form = MyBookForm(request.POST)

        if form.is_valid():
            book_name = form.cleaned_data['title']
            # Проверете дали книгата вече съществува
            existing_book = MyBook.objects.filter(title__icontains=book_name, profile=profile).first()

            if not existing_book:

                # Ако книгата не съществува, я създайте
                new_book = form.save(commit=False)
                new_book.save()
                new_book.profile.add(profile)

                profile.save()

                return redirect('my-books') # Пренасочете към списъка с книги
            else:
                existing_book.profile.add(profile)
                profile.save()
                return redirect('my-books')

        # Ако формата не е валидна, покажете отново формата с грешките
        return render(request, self.template_name, {'form': form})


@login_required
def edit_book(request, pk):
    book = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        form = MyBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('my-books')
    else:
        form = MyBookForm(instance=book)
    return render(request, 'books/my-book-add.html', {'form': form, 'action': 'Edit Book'})


@login_required
def delete_book(request, pk):
    book = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('my-books')
    return render(request, 'books/my-book-delete.html', {'book': book})


class WishListView(LoginRequiredMixin, ListView):
    model = MyBook
    template_name = 'books/wish-list.html'
    context_object_name = 'books'

    def get_queryset(self):
        # Show only books on the user's wish list
        return MyBook.objects.filter(profile=self.request.user.profile, wish_list=True)

    def post(self, request):
        """Обработва изпращането на формата."""
        profile = request.user.profile  # Вземете профила на текущия потребител
        form = MyBookForm(request.POST)

        if form.is_valid():
            book_name = form.cleaned_data['title']
            # Проверете дали книгата вече съществува
            existing_book = MyBook.objects.filter(title__icontains=book_name, profile=profile).first()

            if not existing_book:

                # Ако книгата не съществува, я създайте
                new_book = form.save(commit=False)
                new_book.save()
                new_book.profile.add(profile)

                profile.save()

                return redirect('profile-details') # Пренасочете към списъка с книги
            else:
                existing_book.wish_list = True
                existing_book.profile.add(profile)
                profile.save()

                return redirect('profile-details')

        # Ако формата не е валидна, покажете отново формата с грешките
        return render(request, self.template_name, {'form': form})

@login_required
def delete_from_wishlist(request, pk):
    book = MyBook.objects.get(pk=pk)
    if request.method == "POST":
        book.wish_list = False
        book.save()
        return redirect('my-books')
    return render(request, 'accounts/profile-details.html', {'book': book} )