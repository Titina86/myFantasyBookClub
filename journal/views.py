from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView

from books.models import MyBook
from booksList.models import BooksList
from .models import ReadingJournal
from .forms import ReadingJournalAddForm


class BooksWithJournalListView(LoginRequiredMixin, ListView):
    model = ReadingJournal
    template_name = 'journal/reading-journal.html'
    context_object_name = 'journals'

    def get_queryset(self):
        # Връщаме само дневниците на текущия потребител
        # и само за тези книги от списъка с книги, които имат попълнен дневник.
        return ReadingJournal.objects.filter(
            books_list__profile=self.request.user.profile
        ).select_related('books_list__book')


class CreateReadingJournalView(LoginRequiredMixin, CreateView):
    model = ReadingJournal
    form_class = ReadingJournalAddForm
    template_name = 'journal/journal-create.html'
    success_url = reverse_lazy('reading-journal')  # Пренасочване към списъка с дневници след успешното добавяне
    # Пренасочване към списъка с дневници
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Предаваме текущия потребител
        return kwargs

class BookJournalDetailView(LoginRequiredMixin, DetailView):

    model = ReadingJournal
    template_name = 'journal/journal-book-details.html'
    context_object_name = 'journal'



    def get_queryset(self):

        # return ReadingJournal.objects.filter(books_list__profile=self.request.user.profile)
        return ReadingJournal.objects.filter(
            books_list__profile=self.request.user.profile
        ).select_related('books_list__book')

class EditBookJournalView(LoginRequiredMixin, UpdateView):
    model = ReadingJournal
    form_class = ReadingJournalAddForm
    template_name = 'journal/journal-book-edit.html'
    success_url = reverse_lazy('journal-book-details')  # Пренасочване след успешна редакция

    def get_form_kwargs(self):
        """
        Предайте текущия потребител във формата, за да могат да се филтрират книгите на профила.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        """
        Уверете се, че потребителят редактира само свои дневници.
        """
        obj = super().get_object(queryset)
        if obj.books_list.profile != self.request.user.profile:
            raise PermissionDenied("You are not allowed to edit this journal.")
        return obj

    def form_valid(self, form):
        """On successful form submission, save the changes and redirect"""
        form.save()
        return redirect('reading-journal')

class DeleteBookJournalView(LoginRequiredMixin, DeleteView):
    model = ReadingJournal
    template_name = 'journal/journal-book-delete.html'
    success_url = reverse_lazy('reading-journal')

    def get_queryset(self):
        # Ограничаваме достъпа до дневниците само на текущия потребител
        return ReadingJournal.objects.filter(
            books_list__profile=self.request.user.profile
        )