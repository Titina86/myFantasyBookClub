from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','email', 'profile_picture']


# class CombinedRegistrationForm(forms.Form):
#     user_form = AppUserCreationForm()
#     profile_form = ProfileForm()
#
#     def save(self, commit=True):
#         # Запазване на данните от двете форми
#         user = self.user_form.save(commit=False)
#         user.set_password(self.user_form.cleaned_data['password1'])
#         if commit:
#             user.save()
#             profile = self.profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#         return user
class CombinedRegistrationForm(forms.Form):
    def __init__(self, data=None, files=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Предаваме данните и файловете към подформите
        self.user_form = AppUserCreationForm(data)
        self.profile_form = ProfileForm(data, files)

    def is_valid(self):
        """Проверява валидността на двете форми."""
        return self.user_form.is_valid() and self.profile_form.is_valid()

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Cannot save the form as it is invalid.")

        # Запазваме потребителя
        user = self.user_form.save(commit=False)
        user.set_password(self.user_form.cleaned_data['password1'])
        if commit:
            user.save()

        # Запазваме профила
        profile = self.profile_form.save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_picture']