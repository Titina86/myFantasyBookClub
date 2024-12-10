from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User

from accounts.models import AppUser
from .models import Profile, MyBook, BooksList

class MyBookListViewTest(TestCase):

    def setUp(self):
        # Създаване на тестов потребител и профил
        self.user1 = AppUser.objects.create_user(username='user1', password='password1')
        self.user2 = AppUser.objects.create_user(username='user2', password='password2')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

        # Създаване на книги
        self.book1 = MyBook.objects.create(title='Book 1')
        self.book2 = MyBook.objects.create(title='Book 2')
        self.book3 = MyBook.objects.create(title='Book 3')

        # Добавяне на книги към списъка на различни потребители
        self.books_list1 = BooksList.objects.create(profile=self.profile1, book=self.book1)
        self.books_list2 = BooksList.objects.create(profile=self.profile1, book=self.book2)
        self.books_list3 = BooksList.objects.create(profile=self.profile2, book=self.book3)

    def test_my_books_list_view(self):
        # Вход на потребителя
        self.client.login(username='user1', password='password1')

        # Извикване на изгледа
        response = self.client.get(reverse('my-books'))

        # Уверете се, че отговорът е успешен
        self.assertEqual(response.status_code, 200)

        # Проверете дали правилният шаблон се използва
        self.assertTemplateUsed(response, 'books/my-list-books.html')
    def test_profile_rigth_book(self):
        response = self.client.get(reverse('my-books'))
        # Проверете дали се показват само книгите на потребителя
        books = response.context['books']
        self.assertEqual(len(books), 2)  # Само book1 и book2 трябва да са тук
        self.assertIn(self.books_list1, books)
        self.assertIn(self.books_list2, books)
        self.assertNotIn(self.books_list3, books)  # Тази книга не принадлежи на user1

    def test_my_books_list_view_no_books(self):
        # Вход на потребител без книги
        self.client.login(username='user2', password='password2')

        # Извикване на изгледа
        response = self.client.get(reverse('my-books'))  # Заменете 'my-books-list' с вашето име на пътя

        # Уверете се, че отговорът е успешен
        self.assertEqual(response.status_code, 200)

        # Проверете дали няма книги в контекста
        books = response.context['books']
        self.assertEqual(len(books), 1)  # book3 принадлежи само на user2
        self.assertIn(self.books_list3, books)
