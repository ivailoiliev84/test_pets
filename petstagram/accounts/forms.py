from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from petstagram.accounts.models import Profile
from petstagram.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class PetstagramUserRegisterForm(BootstrapFormMixin, UserCreationForm):
    # bot_catcher = forms.CharField(
    #     max_length=30,
    #     widget=forms.HiddenInput(),
    # )
    #
    # def clean_bot_catcher(self):
    #     bot = self.cleaned_data['bot_catcher']
    #     if bot:
    #         raise ValidationError('Bot detected')

    class Meta:
        model = UserModel
        fields = ('username',)



class PetstagramLoginForm(BootstrapFormMixin, forms.Form):
    user = None
    username = forms.CharField(
        max_length=30,
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(),
    )

    def clean_password(self):
        self.user = authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],

        )

        if not self.user:
            raise ValidationError('Username and/or password are incorrect!')

    def save_user(self):
        return self.user


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'profile_picture': forms.FileInput(),
        }
