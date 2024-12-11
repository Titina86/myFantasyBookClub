from django.test import TestCase

from books.models import MyBook


class TestBookModel(TestCase):
    def setUp(self):
        self.book1 = MyBook.objects.create(title='Book 1')

    def test_book_title_method(self):
        self.assertEqual(str(self.book1), 'Book 1')