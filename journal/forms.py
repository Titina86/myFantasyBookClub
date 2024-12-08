from django import forms

from books.models import MyBook
from booksList.models import BooksList
from .models import ReadingJournal


class ReadingJournalAddForm(forms.ModelForm):
    book_title = forms.CharField(max_length=255, label="Book Title")

    class Meta:
        model = ReadingJournal
        fields = [
            'book_title', 'characters', 'favorite_character', 'start_date', 'end_date',
            'pages', 'favorite_moment', 'about', 'recommended_by',
            'quotes', 'will_recommend_to_friend',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Предаваме текущия потребител
        super().__init__(*args, **kwargs)

    def clean_book_title(self):
        book_title = self.cleaned_data['book_title']

        # Намиране на книгата в списъка на потребителя
        try:
            book_entry = BooksList.objects.get(
                profile=self.user.profile,
                book__title=book_title,
            )
        except BooksList.DoesNotExist:
            raise forms.ValidationError("This book is not in your list.")

        return book_entry

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.books_list = self.cleaned_data['book_title']  # Свързване на дневника с BooksList
        if commit:
            instance.save()
        return instance