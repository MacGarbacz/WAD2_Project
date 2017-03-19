from django import forms
from django.contrib.auth.models import User
from vgc.models import UserProfile, VideoGame, Character, Rating , ListElement

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class DeactivateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

    def __init__(self, *args, **kwargs):
        super(DeactivateUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = "Check this box if you are sure you want to delete this account."

    def clean_is_active(self):
        # Reverses true/false for your form prior to validation
        #
        # You can also raise a ValidationError here if you receive
        # a value you don't want, to prevent the form's is_valid
        # method from return true if, say, the user hasn't chosen
        # to deactivate their account
        is_active = not(self.cleaned_data["is_active"])
        return is_active

class VideoGameForm(forms.ModelForm):
    #name = forms.CharField(max_length=128,
           #                help_text='Please enter the videogame title.')
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = VideoGame
        fields = ('name','picture')
		
class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0, max_value=100)
    class Meta:
        model = Rating
        fields = ('user', 'character', 'rating',)
        exclude = ('user', 'character')


class ListElementForm(forms.ModelForm):
    class Meta:
        model = ListElement
        fields = ('user', 'position','character',)
        exclude = ('user', 'position')



class CharacterForm(forms.ModelForm):

    """Moved this into model, using fields instead
    name = forms.CharField(max_length=128,
                            help_text='Please enter the name of the character.')
    url = forms.URLField(max_length=200,
                         help_text='Please enter the URL of the character.')
    bio = forms.CharField(max_length=512,
                            help_text='Please enter the bio of the character.')
    """

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Character
        fields = ('name','url','bio','picture')
        exclude = ('videogame', )

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
