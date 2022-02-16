from django.urls import path

from petstagram.accounts.views import signup_user, signin_user, signout_user, profile_user

urlpatterns = (
    path('sign-up/', signup_user, name='sign up'),
    path('sign-in/', signin_user, name='sign in'),
    path('sign-out/', signout_user, name='sign out'),
    path('profile/', profile_user, name='profile user'),

)