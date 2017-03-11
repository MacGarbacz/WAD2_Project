from django import template
from vgc.models import VideoGame

register = template.Library()

@register.inclusion_tag('vgc/games.html')
def get_videogame_list():
    return{'games': VideoGame.objects.all()}