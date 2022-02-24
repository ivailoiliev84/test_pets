from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from petstagram.accounts.models import Profile
from petstagram.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class PetstagramUserRegisterForm(BootstrapFormMixin, UserCreationForm):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_bot_catcher(self):
        bot_catcher = self.cleaned_data['bot_catcher']
        if bot_catcher:
            raise forms.ValidationError('Bot detected')

    class Meta:
        model = UserModel
        fields = ('username',)


class PetstagramLoginForm(BootstrapFormMixin, forms.Form):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_bot_catcher(self):
        bot_catcher = self.cleaned_data['bot_catcher']
        if bot_catcher:
            raise forms.ValidationError('Bot detected')

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


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_picture',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'profile_picture': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL'}),

        }


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Enter email'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter descriptions', 'row': 3})
        }
