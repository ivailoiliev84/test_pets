from django.contrib import admin

# Register your models here.
from petstagram.accounts.models import PetstagramUser


@admin.register(PetstagramUser)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username',)
