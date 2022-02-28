from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from petstagram.accounts.forms import PetstagramUserRegisterForm, PetstagramLoginForm, ProfileCreateForm, \
    ProfileUpdateForm
from petstagram.accounts.models import Profile
from petstagram.pets.models import Pet


class RegisterView(CreateView):
    form_class = PetstagramUserRegisterForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('pet list')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


# def signup_user(request):
#     if request.method == 'POST':
#         form = PetstagramUserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             return redirect('sign in')
#
#     else:
#         form = PetstagramUserRegisterForm()
#     context = {
#         'form': form
#     }
#
#     return render(request, 'accounts/signup.html', context)


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
def profile_details(request):
    profile = Profile.objects.get(pk=request.user.id)
    pets = Pet.objects.filter(user_id=request.user.id)

    profile_pets = Pet.objects.filter(user_id=request.user.id).count()

    # pet_photo_like = sum(pp.like for pp in PetPhoto.objects.filter(tagged_pet__user_profile=profile).distinct())

    context = {
        'profile': profile,
        'profile_pets': profile_pets,
        # 'pet_photo_like': pet_photo_like,
        'pets': pets,

    }
    return render(request, 'profile_templates/profile_details.html', context)


def create_profile(request):
    user_profile = Profile.objects.get(pk=request.user.id)
    if request.method == "POST":
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ProfileCreateForm()

    context = {
        'form': form,
        'user_profile': user_profile,
    }

    return render(request, 'profile_templates/profile_create.html', context)


def edit_profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile user')

    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,

    }
    return render(request, 'profile_templates/profile_edit.html', context)


def delete_profile(request):
    user = request.user
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        profile.delete()
        user.delete()
        return redirect('landing')
    else:
        return render(request, 'profile_templates/profile_delete.html')
