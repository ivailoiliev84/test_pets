from django.urls import path

from petstagram.accounts.signals import create_profile
from petstagram.accounts.views import signin_user, signout_user, \
    delete_profile, RegisterView, ProfilePetsList, ProfileDetailsView,  edit_profile

urlpatterns = (
    path('sign-up/', RegisterView.as_view(), name='sign up'),
    # path('sign-up/', signup_user, name='sign up'),
    path('sign-in/', signin_user, name='sign in'),
    path('sign-out/', signout_user, name='sign out'),

    # path('profile/', profile_details, name='profile user'),

    path('profile/', ProfileDetailsView.as_view(), name='profile'),

    path('profile/create/', create_profile, name='create profile'),

    path('profile/edit/', edit_profile, name='edit profile'),
    # path('profile/edit/', ProfileEditView.as_view(), name='edit profile'),

    path('profile/delete/', delete_profile, name='delete profile'),
    path('profile/pets/', ProfilePetsList.as_view(), name='profile pets')

)
