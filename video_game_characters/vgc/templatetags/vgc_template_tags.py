from django import template
from vgc.models import VideoGame, Character, UserProfile, Ratings

register = template.Library()

@register.inclusion_tag('vgc/games.html')
def get_videogame_list():
    return{'games': VideoGame.objects.order_by("name")}

@register.inclusion_tag('vgc/characters.html')
def get_character_list():
    return{"characters": Character.objects.order_by("name")}

@register.inclusion_tag('vgc/characters.html')
def get_rating_list():
    return{"characters": Character.objects.order_by("ratings")}

@register.inclusion_tag('vgc/characters.html')
def get_recommendation_list():
    # This is really hard
    return