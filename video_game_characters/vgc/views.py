from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vgc.forms import UserForm, UserProfileForm, VideoGameForm, CharacterForm, RatingForm , ListElementForm ,DeactivateUserForm
from django.core.urlresolvers import reverse , reverse_lazy
from datetime import datetime
from django.contrib.auth.models import User
from vgc.models import UserProfile , Character, VideoGame , Rating, ListElement


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
    context_dict = {}
    form = UserProfileForm(instance = request.user.profile_user)
    form1 = UserProfileForm()
    context_dict['form'] = form
    context_dict['form1'] = form1

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

def toprated(request):
    return render(request, 'vgc/toprated.html')


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

    def updatelist(userprofile,position,character):
        ListElement.objects.filter(user=userprofile, character=character).delete()
        ListElement.objects.filter(user=userprofile, position=position).delete()
        pos1 = ListElement.objects.create(user=userprofile, position=position, character=character)
        pos1.save()
        return


    context_dict = {}
    form1 = ListElementForm()
    form2 = ListElementForm()
    form3 = ListElementForm()
    form4 = ListElementForm()
    form5 = ListElementForm()
    form6 = ListElementForm()
    form7 = ListElementForm()
    form8 = ListElementForm()
    form9 = ListElementForm()
    form10 = ListElementForm()

    userprofile = UserProfile.objects.get(user=request.user.id)
    if request.method == 'POST':
        post = request.POST
        print(post)
        if post["character"] != "":
            character = Character.objects.get(id=post["character"])

            if "submit_1" in request.POST:
                form1 = ListElementForm(request.POST)
                if form1.is_valid():
                    position = 1
                    updatelist(userprofile, position, character)
                else:
                    print(form1.errors)


            elif "submit_2" in request.POST:
                form2 = ListElementForm(request.POST)
                if form2.is_valid():
                    position = 2
                    updatelist(userprofile, position, character)
                else:
                    print(form2.errors)

            elif "submit_3" in request.POST:
                form3 = ListElementForm(request.POST)
                if form3.is_valid():
                    position = 3
                    updatelist(userprofile, position, character)
                else:
                    print(form4.errors)

            elif "submit_4" in request.POST:
                form4 = ListElementForm(request.POST)
                if form4.is_valid():
                    position = 4
                    updatelist(userprofile, position, character)
                else:
                    print(form4.errors)

            elif "submit_5" in request.POST:
                form5 = ListElementForm(request.POST)
                if form5.is_valid():
                    position = 5
                    updatelist(userprofile, position, character)
                else:
                    print(form5.errors)

            elif "submit_6" in request.POST:
                form6 = ListElementForm(request.POST)
                if form6.is_valid():
                    position = 6
                    updatelist(userprofile, position, character)
                else:
                    print(form6.errors)

            elif "submit_7" in request.POST:
                form7 = ListElementForm(request.POST)
                if form7.is_valid():
                    position = 7
                    updatelist(userprofile, position, character)
                else:
                    print(form7.errors)

            elif "submit_8" in request.POST:
                form8 = ListElementForm(request.POST)
                if form8.is_valid():
                    position = 8

                    updatelist(userprofile, position, character)
                else:
                    print(form8.errors)

            elif "submit_9" in request.POST:
                form9 = ListElementForm(request.POST)
                if form9.is_valid():
                    position = 9
                    updatelist(userprofile, position, character)
                else:
                    print(form9.errors)

            elif "submit_10" in request.POST:
                form10 = ListElementForm(request.POST)
                if form10.is_valid():
                    position = 10
                    updatelist(userprofile, position, character)
                else:
                    print(form10.errors)


    try:
        list = ListElement.objects.all().filter(user=userprofile).order_by("position")

        context_dict['pos1'] = False
        context_dict['pos2'] = False
        context_dict['pos3'] = False
        context_dict['pos4'] = False
        context_dict['pos5'] = False
        context_dict['pos6'] = False
        context_dict['pos7'] = False
        context_dict['pos8'] = False
        context_dict['pos9'] = False
        context_dict['pos10'] = False


        if ListElement.objects.filter(user=userprofile ,position =1).exists():
            context_dict['pos1'] = True
        if ListElement.objects.filter(user=userprofile ,position =2).exists():
            context_dict['pos2'] = True
        if ListElement.objects.filter(user=userprofile ,position =3).exists():
            context_dict['pos3'] = True
        if ListElement.objects.filter(user=userprofile ,position =4).exists():
            context_dict['pos4'] = True
        if ListElement.objects.filter(user=userprofile ,position =5).exists():
            context_dict['pos5'] = True
        if ListElement.objects.filter(user=userprofile ,position =6).exists():
            context_dict['pos6'] = True
        if ListElement.objects.filter(user=userprofile ,position =7).exists():
            context_dict['pos7'] = True
        if ListElement.objects.filter(user=userprofile ,position =8).exists():
            context_dict['pos8'] = True
        if ListElement.objects.filter(user=userprofile ,position =9).exists():
            context_dict['pos9'] = True
        if ListElement.objects.filter(user=userprofile ,position =10).exists():
            context_dict['pos10'] = True

        context_dict['list'] = list

    except ListElement.DoesNotExist:
        context_dict['list'] = None

    context_dict['form1'] = form1
    context_dict['form2'] = form2
    context_dict['form3'] = form3
    context_dict['form4'] = form4
    context_dict['form5'] = form5
    context_dict['form6'] = form6
    context_dict['form7'] = form7
    context_dict['form8'] = form8
    context_dict['form9'] = form9
    context_dict['form10'] = form10

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