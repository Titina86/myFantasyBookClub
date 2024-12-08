from django import forms
from .models import MyBook


# class MyBookAddForm(forms.ModelForm):
#     class Meta:
#         model = MyBook
#         fields = ['title', 'author']

# class BooksListForm(forms.ModelForm):
#     class Meta:
#         model = BooksList
#         fields = ['read_status']
#         widgets = {
#             'read_status': forms.RadioSelect,  # Избор на статус чрез радио бутони
#         }


