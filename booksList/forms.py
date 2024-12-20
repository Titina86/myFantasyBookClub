from django import forms

from books.models import MyBook
from .models import BooksList


class BooksListAddForm(forms.Form):
    title = forms.CharField(max_length=200, label="Book Title")
    author = forms.CharField(max_length=100, label="Author")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False, label="Description"
    )
    read_status = forms.ChoiceField(
        choices=BooksList.ReadStatus.choices,
        widget=forms.RadioSelect,
        initial=BooksList.ReadStatus.WISH_LIST,
        label="Read Status"
    )

    def save(self, profile):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        description = self.cleaned_data['description']
        read_status = self.cleaned_data['read_status']

        book = MyBook.objects.filter(title=title, ).first()
        if not book:

            book = MyBook.objects.create(
                title=title,
                author=author,
                description=description
            )


        BooksList.objects.get_or_create(
            profile=profile,
            book=book,
            defaults={'read_status': read_status}
        )

        return book


class EditBookForm(forms.Form):

    title = forms.CharField(max_length=200, label="Book Title")
    author = forms.CharField(max_length=100, label="Author")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False, label="Description"
    )
    cover = forms.URLField()

    read_status = forms.ChoiceField(
        choices=BooksList.ReadStatus.choices,
        widget=forms.RadioSelect,
        label="Read Status"
    )

    def __init__(self, *args, **kwargs):

        self.book = kwargs.pop('book', None)
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if self.book:

            self.fields['title'].initial = self.book.title
            self.fields['author'].initial = self.book.author
            self.fields['description'].initial = self.book.description
            self.fields['cover'].initial = self.book.cover
            self.fields['read_status'].initial = self.book.my_list_book.get(profile=self.profile).read_status

    def save(self):

        self.book.title = self.cleaned_data['title']
        self.book.author = self.cleaned_data['author']
        self.book.description = self.cleaned_data['description']
        self.book.cover = self.cleaned_data['cover']
        self.book.save()

        books_list_entry = self.book.my_list_book.get(profile=self.profile)
        books_list_entry.read_status = self.cleaned_data['read_status']
        books_list_entry.save()

        return self.book