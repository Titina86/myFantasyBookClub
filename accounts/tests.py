from django.test import TestCase, Client
from django.urls import reverse

from accounts.forms import ProfileEditForm
from accounts.models import Profile, AppUser


class TestProfileModel(TestCase):
    def setUp(self):
        self.user1 = AppUser.objects.create_user(username='user1', password='password1')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile1.first_name = 'Name1'
        self.profile1.last_name = 'Name2'

    def test_full_name_method(self):
        self.assertEqual(self.profile1.get_full_name(), 'Name1 Name2')


class RegisterTestCase(TestCase):
    def test_create_profile_when_create_user(self):
        self.client = Client()
        self.register_url = reverse('register')
        data = {
            'username': 'user1',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'name1',
            'last_name': 'name2',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_profile_when_create_user_failed(self):
        self.client = Client()
        self.register_url = reverse('register')
        data = {
            'username': 'user2',
            'password1': 'strongpassword123',
            'password2': 'strongpassword',
            'first_name': 'name1',
            'last_name': 'name2',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(AppUser.objects.filter(username='user2').exists())
        self.assertFalse(Profile.objects.exists())


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'name1',
            'last_name': 'name2',
            'email': 'email@email.com',
            'profile_picture': 'http://example.com/image.jpg'
        }

    def test_edit_profile__form_true(self):
        form = ProfileEditForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_edit_profile__form_failed(self):
        self.valid_data['first_name']=''
        form = ProfileEditForm(data=self.valid_data)

        self.assertFalse(form.is_valid())