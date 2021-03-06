from django import template
from vgc.models import VideoGame, Character, UserProfile, Rating , ListElement
from math import *
from django.contrib.auth.models import User
from vgc.utils import *

register = template.Library()

@register.inclusion_tag('vgc/games.html')
def get_videogame_list(user):
    context_dict={}
    context_dict['games'] = VideoGame.objects.order_by("name")
    context_dict['user'] = user
    return context_dict


@register.simple_tag
def update_pos(user,r):
    user1 =  User.objects.get(username=user)
    up = UserProfile.objects.get(user=user1)
    return ListElement.objects.filter(user=up,position =r).exists()




@register.inclusion_tag('vgc/characters.html')
def get_character_list(search):
    if(search == None):
        search = ""
    return{"characters": searchCharacters(search)}#Character.objects.order_by("name")}

#Averages the rating for each character, sorts them based on rating and returns the top 10
@register.inclusion_tag('vgc/top10alltime.html')
def get_rating_list():
    rating_list = []
    character_list = Character.objects.all()
    for c in character_list:
        rate = 0
        ratings = Rating.objects.filter(character=c.pk)
        for r in ratings:
            rate = rate + r.rating / len(ratings)
        rating_list.append((c, rate))
    rating_list = sorted(rating_list, key=lambda rating: rating[1], reverse=True)
    toprated = []
    for i in rating_list:
        toprated.append(i[0])
    return{"characters": toprated[:10]}


@register.inclusion_tag('vgc/recommendations2.html', takes_context=True)
def get_recommendation_list(context):
    request = context['request']
    current_user = request.user.profile_user.id
    current_user = UserProfile.objects.get(pk=current_user)
    # Creates a list of the current users ratings
    current_user_ratings = list(Rating.objects.filter(user = current_user).values_list())
    # Creates a list of every other users ratings
    all_user_ratings = list(Rating.objects.exclude(user = current_user).values_list())
    # Gets first user's pk
    user_i = all_user_ratings[0][1]
    rating_list = []
    user_rating_list = []
    most_similar = 999999
    most_similar_user = user_i

    # function checks if item is last in the list
    def last(seq):
        seq = iter(seq)
        a = next(seq)
        for b in seq:
            yield a, False
            a = b
        yield a, True

    for i, is_last in last(all_user_ratings):
        # if we have moved on to a new user or the list has ended
        if i[1] != user_i or is_last:
            # Run similarity algorithm on the sets of ratings
            similarity = sqrt(sum(pow(a-b,2) for a,b in zip(rating_list, user_rating_list)))
            # If the user is the most similar record their similarity and pk
            if similarity < most_similar:
                most_similar = similarity
                most_similar_user = user_i
            user_i = i[1]
            rating_list = []
            user_rating_list = []
        for j in current_user_ratings:
            # if both users have rated the same character add the ratings to sets
            if i[2] == j[2]:
                user_rating_list.append(j[3])
                rating_list.append(i[3])
    # Get a list of the most similar user's ratings
    other_user_list = Rating.objects.filter(user = most_similar_user).values_list()
    recommendation_list = []
    for k in other_user_list:
        rated = False
        for l in current_user_ratings:
            if k[2] == l[2]:
                rated = True
        # If the logged in user has not rated a character and the most similar user has rated that charater > 70, add that character to the recommendation list
        if rated == False and k[3] > 70:
            recommendation_list.append(k[2])

    return{"characters": Character.objects.filter(pk__in=recommendation_list)}