import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'video_game_characters.settings')

import django
django.setup()
from vgc.models import VideoGame, Character

def populate():


    Jude = [
        {"name": "Jude",
        "url":"",
        "bio": "its me"}, ]


    cats = {"Game1": {"characters": Jude},}

    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data["characters"]:
            add_page(c, p["name"], p["url"], p["bio"])


# Print out the Games we have added.
    for c in VideoGame.objects.all():
        for p in Character.objects.filter(videogame=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, name, url, bio):
    p = Character.objects.get_or_create(videogame=cat, name=name)[0]
    p.url=url
    p.bio=bio
    p.save()
    return p

def add_cat(name):
    c = VideoGame.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()