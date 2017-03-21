import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'video_game_characters.settings')

import django
import random
django.setup()
from vgc.models import VideoGame, Character , UserProfile , ListElement , Rating
from django.contrib.auth.models import User

def populate():


    Jude = [{"name": "Jude",
             "url":"",
             "bio": "its me" ,
             "picture" :"char_images/DrSuvi.jpg"}]


    Dr_Suvi=[{"name": "Dr. Suvi Anwar",
              "url":"http://masseffect.wikia.com/wiki/Dr._Suvi_Anwar",
              "bio": "Dr. Suvi Anwar is a member of the Nexus’ science team, and holds advanced degrees in astrophysics and molecular biology. In a screening interview, she stated that she was from a “large, rather boisterous family” of five children." ,
              "picture" : "char_images/DrSuvi.jpg"}]

    Shepard = [{"name": "Commander Shepard",
             "url": "http://masseffect.wikia.com/wiki/Commander_Shepard",
             "bio": "Shepard was born on April 11, 2154, is a graduate of the Systems Alliance N7 special forces program (service no. 5923-AC-2826), a veteran of the Skyllian Blitz, and is initially assigned to the SSV Normandy in 2183 as Executive Officer.",
             "picture": "char_images/MassEffect3_Shepard.jpg"}]

    JamesVega = [{"name": "James Vega",
             "url": "http://masseffect.wikia.com/wiki/James_Vega",
             "bio": "Lieutenant James Vega is a human Systems Alliance Marine and a member of Commander Shepard's squad in 2186.",
             "picture": "char_images/James_Vega.png"}]

    KaidanAlenko = [{"name": "Kaidan Alenko",
             "url": "http://masseffect.wikia.com/wiki/Kaidan_Alenko",
             "bio": "Kaidan Alenko is a human Sentinel and a Systems Alliance Marine. While serving aboard the SSV Normandy, he is a Staff Lieutenant and head of the ship's Marine detail. ",
             "picture": "char_images/Kaidan.png"}]

    Jack_Subject_Zero = [{"name": "Jack-Subject Zero",
             "url":"http://masseffect.wikia.com/wiki/Jack",
             "bio": "Jack, also known as Subject Zero, is a notorious criminal whose crimes include piracy, kidnapping, vandalism and murder. " ,
             "picture" :"char_images/Subject_Zero.png"}]

    John_117 = [{"name": "John-117",
             "url": "http://halo.wikia.com/wiki/John-117",
             "bio": "The Master Chief, is a Spartan-II commando of the UNSC Naval Special Warfare Command who became one of the most important UNSC heroes during the Human-Covenant war.",
             "picture": "char_images/John117.png"}]

    Cortana = [{"name": "Cortana",
             "url": "http://halo.wikia.com/wiki/Cortana",
             "bio": "Cortana, UNSC Artificial intelligence (SN: CTN 0452-9), is a smart artificial intelligence construct. ",
             "picture": "char_images/Cortana.png"}]

    Avery_Johnson = [{"name": "Avery Johnson",
             "url": "http://halo.wikia.com/wiki/Avery_Johnson",
             "bio": "Sergeant Major Avery Junior Johnson (SN: 48789-20114-AJ ) was a Human senior non-commissioned officer who served with the UNSC Marine Corps during the Insurrection and Human-Covenant war.",
             "picture": "char_images/SgtJohnson.png"}]

    Jacob_Keyes = [{"name": "Jacob Keyes",
             "url": "http://halo.wikia.com/wiki/Jacob_Keyes",
             "bio": "Captain Jacob Keyes (SN: 01928-19912-JK) was a legendary naval officer and one of the most brilliant tacticians in the UNSC Navy.",
             "picture": "char_images/Jacob_Keyes.png"}]

    John_Forge = [{"name": "John Forge",
             "url": "http://halo.wikia.com/wiki/John_Forge",
             "bio": "Sergeant John Forge (Service Number 63492-94758-JF) was a veteran non-commissioned officer and an infantryman in the UNSC Marine Corps.",
             "picture": "char_images/JohnForge.png"}]

    Lucy_Stillman = [{"name": "Lucy Stillman",
             "url": "http://assassinscreed.wikia.com/wiki/Lucy_Stillman",
             "bio": "Lucy Stillman (1988 – 2012) was a member of the Assassin Order and a genetic memory researcher for Abstergo Industries' Animus Project",
             "picture": "char_images/Lucy.png"}]

    Edward_Kenway = [{"name": "Edward Kenway",
             "url": "http://assassinscreed.wikia.com/wiki/Edward_Kenway",
             "bio": "Edward James Kenway (1693 – 1735) was a Welsh-born British privateer-turned-pirate and a member of the Assassin Order.",
             "picture": "char_images/Edward.png"}]

    Ezio_Auditore = [{"name": "Ezio Auditore da Firenze",
             "url": "http://assassinscreed.wikia.com/wiki/Ezio_Auditore_da_Firenze",
             "bio": "Ezio Auditore da Firenze (1459 – 1524) was a Florentine nobleman during the Renaissance, and, unbeknownst to most historians and philosophers, the Mentor of the Italian Brotherhood of Assassins, a title which he held from 1503 to 1513.",
             "picture": "char_images/Ezio.png"}]

    Altair = [{"name": "Altair",
             "url": "http://assassinscreed.wikia.com/wiki/Alta%C3%AFr_Ibn-La%27Ahad",
             "bio": "Altaïr Ibn-La'Ahad (1165 – 1257) was a Syrian-born member of the Levantine Brotherhood of Assassins and served as their Mentor from 1191 until his death in 1257. ",
             "picture": "char_images/Altair.png"}]

    Desmond_Miles = [{"name": "Desmond Miles",
             "url": "http://assassinscreed.wikia.com/wiki/Desmond_Miles",
             "bio": "Desmond Miles (1987 – 2012) was a member of the Assassin Order and a descendant of numerous familial lines that had sworn an allegiance to the Assassins",
             "picture": "char_images/Desmond.png"}]


    games = {"Mass Effect": {"characters": [Dr_Suvi ,Shepard,JamesVega,KaidanAlenko,Jack_Subject_Zero] , "picture": "game_images/ac.jpg"},
            "Halo": {"characters": [John_117, Cortana, Jacob_Keyes, Avery_Johnson, John_Forge], "picture":"game_images/halo.jpg"},
            "Assassin's Creed": {"characters": [Desmond_Miles, Altair, Ezio_Auditore, Edward_Kenway, Lucy_Stillman] , "picture":"game_images/masseffect.jpg"}
            }

    userlist={"Jude": {"username": "Jude", "email": "jude@gmail.com", "password": "password","picture": "profile_images/JudeProf.png"},
              "Andrew": {"username": "Andrew", "email": "andrew@gmail.com", "password": "password","picture": "profile_images/AndrewProf.png"},
              "Maciej": {"username": "Maciej", "email": "maciej@gmail.com", "password": "password","picture": "profile_images/MaciejProf.png"},
              "Henry": {"username": "Henry", "email": "henry@ymail.com", "password": "password","picture": "profile_images/HenryProf.png"},
              }




    # If you want to add more catergories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary properly.

    for games, game_data in games.items():
        c = add_game(games,game_data["picture"])
        for k in game_data["characters"]:
            for p in k:
                add_character(c, p["name"], p["url"], p["bio"],p["picture"])

    add_user(userlist)
    add_toptens()
    add_ratings()



# Print out the Games we have added.
    for c in VideoGame.objects.all():
        for p in Character.objects.filter(videogame=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_character(cat, name, url, bio,picture):
    p = Character.objects.get_or_create(videogame=cat, name=name)[0]
    p.url=url
    p.bio=bio
    p.picture = picture
    p.save()
    return p

def add_game(name,picture):
    c = VideoGame.objects.get_or_create(name=name)[0]
    c.picture = picture
    c.save()
    return c


def add_user(userlist):
    for tobeuser,userdata in userlist.items():
        u = User.objects.create_user( userdata["username"] , email = userdata["email"],password = userdata["password"])
        up = UserProfile.objects.create(user=u)
        up.save()
        up.picture = userdata["picture"]
        up.save()


def add_toptens():
    up = UserProfile.objects.all()
    allchars = Character.objects.all()
    jars =[]
    for i in allchars:
        jars.append(i.name)

    for user in up:
        chars = list(jars)
        for pos in range(1, 11):
            charactername = random.choice(chars)
            character = Character.objects.get(name=charactername)
            l = ListElement.objects.create(user=user,position = pos , character = character )
            l.save()
            chars.remove(charactername)

def add_ratings():
    up = UserProfile.objects.all()
    allchars = Character.objects.all()

    for user in up:
        for character in allchars:
            l = Rating.objects.create(user=user, character=character,rating = random.choice(range(101)))
            l.save()


# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()