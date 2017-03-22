from django import template
from vgc.models import VideoGame, Character, UserProfile, Rating
from math import *

register = template.Library()

@register.inclusion_tag('vgc/games.html')
def get_videogame_list(user):
    context_dict={}
    context_dict['games'] = VideoGame.objects.order_by("name")
    context_dict['user'] = user
    return context_dict


@register.inclusion_tag('vgc/characters.html')
def get_character_list():
    return{"characters": Character.objects.order_by("name")}

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
    print (rating_list)
    for i in rating_list:
        toprated.append(i[0])
    print (toprated)
    return{"characters": toprated[:10]}

@register.inclusion_tag('vgc/recommendations2.html', takes_context=True)
def get_recommendation_list(context):
    request = context['request']
    current_user = request.user.profile_user.id
    current_user = UserProfile.objects.get(pk=current_user)
    current_user_ratings = list(Rating.objects.filter(user = current_user).values_list())
    all_user_ratings = list(Rating.objects.exclude(user = current_user).values_list())
    #print (current_user_ratings)
    #print (all_user_ratings)
    user_i = all_user_ratings[0][1]
    rating_list = []
    user_rating_list = []
    most_similar = 999999
    most_similar_user = user_i
    for i in all_user_ratings:
        if i[1] != user_i:
            similarity = sqrt(sum(pow(a-b,2) for a,b in zip(rating_list, user_rating_list)))
            if similarity < most_similar:
                most_similar = similarity
                most_similar_user = user_i
            user_i = i[1]
            rating_list = []
            user_rating_list = []
        for j in current_user_ratings:
            if i[2] == j[2]:
                user_rating_list.append(j[3])
                rating_list.append(i[3])
    other_user_list = Rating.objects.filter(user = most_similar_user).values_list()
    recommendation_list = []
    for k in other_user_list:
        rated = False
        for l in current_user_ratings:
            if k[2] == l[2]:
                rated = True
        if rated == False and k[3] > 70:
            recommendation_list.append(k[2])

    #print (recommendation_list)
    return{"characters": Character.objects.filter(pk__in=recommendation_list)}