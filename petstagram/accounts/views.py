from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView

from petstagram.accounts.forms import PetstagramUserRegisterForm, PetstagramLoginForm, ProfileForm
from petstagram.accounts.models import Profile
from petstagram.pets.models import Pet


def signup_user(request):
    if request.method == 'POST':
        form = PetstagramUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign in')

    else:
        form = PetstagramUserRegisterForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/signup.html', context)


def signin_user(request):
    if request.method == 'POST':
        form = PetstagramLoginForm(request.POST)
        if form.is_valid():
            user = form.save_user()
            login(request, user)
            return redirect('pet list')
    else:
        form = PetstagramLoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


def signout_user(request):
    logout(request)
    return redirect('landing')


# class ProfileDetailView(FormView):
#     template_name = 'accounts/user_profile.html'
#     form_class = ProfileForm
#     success_url = reverse_lazy('profile user')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = Profile.objects.get(pk=self.request.user.id)
#         user_pets = Pet.objects.filter(pk=self.request.user.id)
#
#         context['pets'] = user_pets
#         context['profile'] = profile
#         return context


@login_required
def profile_user(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('profile user')

    else:

        form = ProfileForm(instance=profile)

    pets = Pet.objects.filter(user_id=request.user.id)
    context = {
        'form': form,
        'pets': pets,
        'profile': profile,

    }

    return render(request, 'accounts/user_profile.html', context)
