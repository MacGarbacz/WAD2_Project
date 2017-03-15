from django import template
from vgc.models import VideoGame, Character

register = template.Library()

@register.inclusion_tag('vgc/games.html')
def get_videogame_list():
    return{'games': VideoGame.objects.order_by("name")}

@register.inclusion_tag('vgc/characters.html')
def get_character_list():
    return{"characters": Character.objects.order_by("name")}