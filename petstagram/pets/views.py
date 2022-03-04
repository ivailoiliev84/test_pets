from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from petstagram.common.forms import CommentForm
from petstagram.common.models import Comment
from petstagram.pets.forms import CreatePetForm, EditPetForm
from petstagram.pets.models import Pet, Like

UserModel = get_user_model()


# def pet_all(request):
#     pets = Pet.objects.all()
#
#     context = {
#         'pets': pets
#     }
#     return render(request, 'pets/pet_list.html', context)

class PetList(ListView):
    template_name = 'pets/pet_list.html'
    model = Pet
    context_object_name = 'pets'



    


def pet_details(request, pk):
    pet = Pet.objects.get(pk=pk)
    pet.like_count = pet.like_set.count()

    is_owner = pet.user == request.user
    like_object_by_user = pet.like_set.filter(user_id=request.user.id).first()

    context = {
        'pet': pet,
        'comment_form': CommentForm(),
        'comments': pet.comment_set.all(),
        'is_owner': is_owner,
        'is_like': like_object_by_user is not None,
    }

    return render(request, 'pets/pet_detail.html', context)


@login_required
def comment_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    form = CommentForm(request.POST)
    user_who_comment = pet.comment_set.filter(user_id=request.user.id).first()

    if form.is_valid():
        comment = Comment(
            comment=form.cleaned_data['text'],
            pet=pet,
            user=request.user,
        )
        comment.save()
        return redirect('pet details', pet.id)


@login_required
def like_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    user_who_like = pet.like_set.filter(user_id=request.user.id).first()

    if user_who_like:
        user_who_like.delete()
    else:

        like = Like(
            pet=pet,
            user=request.user,

        )
        like.save()

    return redirect('pet details', pet.id)


@login_required
def create_pet(request):
    if request.method == 'POST':
        form = CreatePetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            return redirect('pet list')

    else:
        form = CreatePetForm()

    context = {
        'form': form
    }

    return render(request, 'pets/pet_create.html', context)





@login_required
def edit_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet list')

    else:
        form = EditPetForm(instance=pet)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(request, 'pets/pet_edit.html', context)


@login_required
def delete_pet(request, pk):
    pet = Pet.objects.get(pk=pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('pet list')
    else:
        context = {
            'pet': pet
        }
        return render(request, 'pets/pet_delete.html', context)
