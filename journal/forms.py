from django import forms

from journal.models import ReadingJournal


class ReadingJournalForm(forms.ModelForm):
    class Meta:
        model = ReadingJournal
        fields = [
            'book',
            'characters',
            'favorite_character',
            'start_date',
            'end_date',
            'pages',
            'favorite_moment',
            'about',
            'recommended_by',
            'quotes',
            'will_recommend_to_friend',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'quotes': forms.Textarea(attrs={'rows': 3}),
            'about': forms.Textarea(attrs={'rows': 5}),
        }