from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vgc.forms import UserForm, UserProfileForm, VideoGameForm, CharacterForm
from django.core.urlresolvers import reverse
from datetime import datetime
from vgc.models import Character, VideoGame , Rating ,ListElement

def index(request):

    return render(request, 'vgc/index.html')

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.

    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,'vgc/register.html',{'user_form': user_form,
                    'profile_form': profile_form,'registered': registered})


def user_profile(request):
    form = UserProfileForm(instance = request.user.profile_user)
    return render(request,'vgc/user_profile.html',{'form': form})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homecharacter.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your VGC account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'vgc/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homecharacter.
    return HttpResponseRedirect(reverse('index'))


def show_listofvideogame(request):
    return render(request, 'vgc/gameslist.html')

def allcharacters(request):
    return render(request, 'vgc/allcharacters.html')


def show_videogame(request, videogame_name_slug):
    context_dict = {}

    try:
        videogame = VideoGame.objects.get(slug=videogame_name_slug)

        characters = Character.objects.filter(videogame=videogame)

        context_dict['characters'] = characters

        context_dict['videogame'] = videogame
    except VideoGame.DoesNotExist:
        context_dict['videogame'] = None
        context_dict['characters'] = None

    return render(request, 'vgc/videogame.html', context_dict)


def show_character(request, character_name_slug):
    context_dict = {}

    try:
        character = Character.objects.get(slug=character_name_slug)

        context_dict['character'] = character

    except Character.DoesNotExist:
        context_dict['character'] = None

    return render(request, 'vgc/characterpage.html', context_dict)



def google_search_verification(request):
    return render(request, 'vgc/googlee7d575755dc66c86.html')


@login_required
def your_top_10(request, user):
    context_dict = {}

    try:
        list = ListElement.objects.filter(user=user)

        context_dict['list'] = list

    except ListElement.DoesNotExist:
        context_dict['list'] = None

    return render(request, 'vgc/your_top_10.html', context_dict)



@login_required
def add_videogame(request):
    form = VideoGameForm()

    if request.method == 'POST':
        form = VideoGameForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)
    return render(request, 'vgc/add_videogame.html', {'form': form})



@login_required
def add_character(request, videogame_name_slug):
    try:
        videogame = VideoGame.objects.get(slug=videogame_name_slug)
    except VideoGame.DoesNotExist:
        videogame = None

    form = CharacterForm()
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            if videogame:
                character = form.save(commit=False)
                character.videogame = videogame
                character.views = 0
                character.save()
                return show_videogame(request, videogame_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'videogame': videogame}
    return render(request, 'vgc/add_character.html', context_dict)