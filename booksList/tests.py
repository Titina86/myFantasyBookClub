from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import AppUser
from .models import Profile, MyBook, BooksList


class BooksListModelTest(TestCase):
    def setUp(self):
        self.user1 = AppUser.objects.create_user(username='user1', password='password1')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.book1 = MyBook.objects.create(title='Book 1')
        self.list_book1 = BooksList.objects.create(profile=self.profile1, book=self.book1)

    def test_book_title_string_method(self):
        self.assertEqual(self.book1.__str__(), 'Book 1')


class MyBookListViewTest(TestCase):

    def setUp(self):

        self.user1 = AppUser.objects.create_user(username='user1', password='password1')
        self.user2 = AppUser.objects.create_user(username='user2', password='password2')
        self.user3 = AppUser.objects.create_user(username='user3', password='password3')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.profile3 = Profile.objects.get(user=self.user3)

        self.book1 = MyBook.objects.create(title='Book 1')
        self.book2 = MyBook.objects.create(title='Book 2')
        self.book3 = MyBook.objects.create(title='Book 3')

        self.list_book1 = BooksList.objects.create(profile=self.profile1, book=self.book1)
        self.list_book2 = BooksList.objects.create(profile=self.profile1, book=self.book2)
        self.list_book3 = BooksList.objects.create(profile=self.profile2, book=self.book3)

    def test_my_books_list_view(self):
        self.client = Client()
        self.client.login(username='user1', password='password1')

        response = self.client.get(reverse('my-books'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'books/my-list-books.html')

    def test_profile_rigth_book(self):
        self.client = Client()
        self.client.login(username='user2', password='password2')
        response = self.client.get(reverse('my-books'))

        books = BooksList.objects.filter(profile=self.profile2)
        self.assertEqual(len(books), 1)
        self.assertIn(self.list_book3, books)

        self.assertNotIn(self.list_book1, books)
        self.assertNotIn(self.list_book2, books)

    def test_my_books_list_view_no_books(self):
        self.client = Client()
        self.client.login(username='user3', password='password3')

        response = self.client.get(reverse('my-books'))
        self.assertEqual(response.status_code, 200)

        books = BooksList.objects.filter(profile=self.profile3)
        self.assertEqual(len(books), 0)
        self.assertNotIn(self.list_book2, books)
