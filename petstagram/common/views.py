from django.shortcuts import render, redirect

# Create your views here.
from petstagram.common.forms import CommentForm
from petstagram.common.models import Comment
from petstagram.pets.models import Pet


def index(request):
    return render(request, 'landing_page.html')



