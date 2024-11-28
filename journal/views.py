from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from books.models import MyBook
from journal.forms import ReadingJournalForm
from journal.models import ReadingJournal


class ReadingJournalListView(ListView):
    model = ReadingJournal
    template_name = 'journal/reading-journal.html'
    context_object_name = 'journals'

    def get_queryset(self):
        return ReadingJournal.objects.filter(user=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add books associated with the user to the context
        context['user_books'] = MyBook.objects.filter(profile=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        if book_id:
            book = MyBook.objects.get(id=book_id)
            if not ReadingJournal.objects.filter(user=self.request.user.profile, book=book).exists():
                ReadingJournal.objects.create(user=self.request.user.profile, book=book)
        return redirect('reading-journal-list')


class ReadingJournalCreateView(LoginRequiredMixin, CreateView):
    model = ReadingJournal
    form_class = ReadingJournalForm
    template_name = 'journal/journal-create.html'
    success_url = reverse_lazy('reading-journal-list')  # Redirect after successful form submission

    def form_valid(self, form):
        # Associate the new journal entry with the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReadingJournalDetailView(LoginRequiredMixin, DetailView):
    model = ReadingJournal
    template_name = 'journal/journal-book-details.html'  # Path to your template
    context_object_name = 'journal'


class ReadingJournalUpdateView(LoginRequiredMixin, UpdateView):
    model = ReadingJournal
    template_name = 'journal/journal-book-edit.html'  # Path to your HTML template
    fields = [
        'book', 'characters', 'favorite_character', 'start_date',
        'end_date', 'pages', 'favorite_moment', 'about',
        'recommended_by', 'quotes', 'will_recommend_to_friend'
    ]
    context_object_name = 'journal'

    def get_success_url(self):
        # Redirect back to the detail view of the updated journal
        return reverse_lazy('journal-book-details', kwargs={'pk': self.object.pk})
