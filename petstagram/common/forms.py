from django import forms


class CommentForm(forms.Form):
    bot_catcher = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_bot_catcher(self):
        bot_catcher = self.cleaned_data['bot_catcher']
        if bot_catcher:
            raise forms.ValidationError('Bot detected')

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control rounded-2',
            }
        ),
    )
