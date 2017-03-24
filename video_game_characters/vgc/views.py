from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vgc.forms import UserForm, UserProfileForm, VideoGameForm, CharacterForm, RatingForm , ListElementForm ,DeactivateUserForm
from django.core.urlresolvers import reverse , reverse_lazy
from datetime import datetime
from django.contrib.auth.models import User
from vgc.models import UserProfile , Character, VideoGame, Rating, ListElement
from .utils import *

def index(request):
    context_dict = {}
    l = {}
    #gets all users apart from the current one if current one is logged in
    if request.user.is_authenticated:
        all_users = User.objects.exclude(pk=request.user.id)
    else:
        all_users = User.objects.all()

    #This adds up to 5 users top ten to the context dict to be displayed in the homepage
    upto5counter = 0
    for u in all_users :
        if u.is_active == True and not u.is_staff and upto5counter <6 :
            userprofile = UserProfile.objects.get(user = u)
            u_in_str_form =  u.username
            if ListElement.objects.all().filter(user_id=userprofile).order_by("position").exists() :
                l[u_in_str_form] = ListElement.objects.all().filter(user_id=userprofile).order_by("position")
                upto5counter += 1

        elif upto5counter <6 :
            all_users.filter(pk=u.id).delete()
    context_dict["l"] = l
    return render(request, 'vgc/index.html' , context_dict)

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

@login_required
def user_profile(request):
    context_dict = {}
    form = UserProfileForm(instance = request.user.profile_user)
    form1 = UserProfileForm()
    context_dict['form'] = form
    context_dict['form1'] = form1

    #Allows user to edit picture
    if request.method =='POST':
        if "edit" in request.POST:
            if 'picture' in request.FILES:
                currentprofile = UserProfile.objects.get(user=request.user)
                currentprofile.picture = request.FILES['picture']
                currentprofile.save()
                form = UserProfileForm(instance=currentprofile)
                context_dict['form'] = form
                return render(request, 'vgc/user_profile.html', context_dict)


    return render(request,'vgc/user_profile.html',context_dict)


@login_required
def deactivate_user_view(request):
    pk = request.user.id
    user = User.objects.get(pk=pk)
    form1 = DeactivateUserForm(instance=user)
    #Allows user to delete their account
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            if "delete" in request.POST:
                form1 = DeactivateUserForm(request.POST, instance=user)
                if form1.is_valid():
                    deactivate_user = form1.save(commit=False)
                    user.is_active = False
                    deactivate_user.save()
                    return user_logout(request)
            elif "back" in request.POST:
                return user_profile(request)
        return render(request, "vgc/userprofile_del.html", {"form1": form1,})
    else:
        raise PermissionDenied


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
                return redirect(index)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your VGC account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'vgc/logininvalid.html')
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
    return redirect(index)


def show_listofvideogame(request):
    return render(request, 'vgc/gameslist.html')

def allcharacters(request):
    context_dict = {"search": request.GET.get("search")}
    return render(request, 'vgc/allcharacters.html', context_dict)

def toprated(request):
    return render(request, 'vgc/toprated.html')

@login_required
def recommendations(request):
    return render(request, 'vgc/recommendations.html', {})

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
        ratings = Rating.objects.all().filter(character = character)
        rate = 0.0
        for r in ratings:
            rate = rate + r.rating/len(ratings)
        context_dict['rating'] = rate
    except Character.DoesNotExist:
        context_dict['character'] = None
        context_dict['rating'] = 0

    return render(request, 'vgc/characterpage.html', context_dict)



def google_search_verification(request):
    return render(request, 'vgc/googlee7d575755dc66c86.html')



@login_required
def your_top_10(request,user):
    #Updates user's ranking of the position given to the character given
    def updatelist(userprofile,position,character):
        ListElement.objects.filter(user=userprofile, character=character).delete()
        ListElement.objects.filter(user=userprofile, position=position).delete()
        pos1 = ListElement.objects.create(user=userprofile, position=position, character=character)
        pos1.save()
        return

    context_dict = {}
    form1 = ListElementForm()

    userprofile = UserProfile.objects.get(user= User.objects.get(username=user))
    context_dict['user1'] = user
    #Gets the character and position from the post by determining name of submit which goes from "1" to "10" for each position
    if request.method == 'POST' and userprofile == request.user.profile_user:
        post = request.POST
        if post["character"] != "":
            character = Character.objects.get(id=post["character"])
            for i in range(1,11):
                s = str(i)
                if s in request.POST:
                    form = ListElementForm(request.POST)
                    if form.is_valid():
                        position = i
                        updatelist(userprofile, position, character)
                    else:
                        print(form.errors)

    try:
        list = ListElement.objects.all().filter(user=userprofile).order_by("position")
        context_dict['list'] = list

    except ListElement.DoesNotExist:
        context_dict['list'] = None

    context_dict['form'] = form1
    context_dict["range"] = range(1,11)

    return render(request, 'vgc/your_top_10.html', context_dict )



@login_required
def add_videogame(request):
    form = VideoGameForm()

    if request.method == 'POST':
        form = VideoGameForm(request.POST)

        if form.is_valid():
            game = form.save(commit=False)
            if 'picture' in request.FILES:
                game.picture = request.FILES['picture']
            game.save()

            return redirect(index)
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
                if 'picture' in request.FILES:
                    character.picture = request.FILES['picture']
                character.save()
                return show_videogame(request, videogame_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'videogame': videogame}
    return render(request, 'vgc/add_character.html', context_dict)
    
@login_required
def rate(request, character_slug):
    try:
        characterObj = Character.objects.get(slug=character_slug)
    except Character.DoesNotExist:
        characterObj = None

    form = RatingForm()
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if characterObj:
                try:
                    rating = Rating.objects.get(user = request.user.profile_user, character = characterObj)
                    rating.rating = request.POST.get('rating')
                except Rating.DoesNotExist:
                    rating = form.save(commit=False)
                    rating.character = characterObj
                    rating.rating = request.POST.get('rating')
                    #assume this exists as login required?
                    rating.user = request.user.profile_user
                rating.save()
                return show_character(request, character_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'character': characterObj}
    return render(request, 'vgc/rate.html', context_dict)