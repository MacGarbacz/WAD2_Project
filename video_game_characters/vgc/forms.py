from django import forms
from django.contrib.auth.models import User
from vgc.models import UserProfile, VideoGame, Character

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class VideoGameForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text='Please enter the videogame title.')
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = VideoGame
        fields = ('name',)

class CharacterForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                            help_text='Please enter the name of the character.')
    url = forms.URLField(max_length=200,
                         help_text='Please enter the URL of the character.')
    bio = forms.CharField(max_length=512,
                            help_text='Please enter the bio of the character.')

    class Meta:
        model = Character
        exclude = ('videogame', )

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
