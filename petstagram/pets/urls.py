from django.urls import path

from petstagram.pets.views import pet_details, like_pet, edit_pet, delete_pet, comment_pet, PetList,  \
    create_pet

urlpatterns = (
    # path('', pet_all, name='pet list'),
    path('', PetList.as_view(), name='pet list'),


    path('details/<int:pk>', pet_details, name='pet details'),
    path('like/<int:pk>', like_pet, name='like'),

    path('create/', create_pet, name='create pet'),


    path('edit/<int:pk>', edit_pet, name='edit pet'),
    path('delete/<int:pk>', delete_pet, name='delete pet'),
    path('comment/<int:pk>', comment_pet, name='comment pet'),

)
