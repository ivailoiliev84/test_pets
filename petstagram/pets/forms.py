from django import forms
from django.core.exceptions import ValidationError

from petstagram.core.forms import BootstrapFormMixin
from petstagram.pets.models import Pet


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
    )

    def clean_bot_catcher(self):
        bot = self.cleaned_data['bot_catcher']
        if bot:
            raise ValidationError('Bot detected')

    class Meta:
        model = Pet
        exclude = ('user',)


class EditPetForm(CreatePetForm):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
    )

    def clean_bot_catcher(self):
        bot = self.cleaned_data['bot_catcher']
        if bot:
            raise ValidationError('Bot detected')

    class Meta:
        model = Pet
        exclude = ('user',)
        widgets = {
            'type': forms.TextInput(
                attrs={
                    'readonly': 'readonly'
                }
            ),
            'image': forms.FileInput()
        }
