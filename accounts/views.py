from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.forms import AppUserCreationForm, CombinedRegistrationForm, ProfileForm, ProfileEditForm
from accounts.models import Profile

UserModel = get_user_model()


# class AppUserRegisterView(CreateView):
#     model = UserModel
#     form_class = AppUserCreationForm
#     template_name = 'accounts/register-page.html'
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)
#         return response

def register(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CombinedRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

