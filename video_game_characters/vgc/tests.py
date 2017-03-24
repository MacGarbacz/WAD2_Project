#coding: utf-8
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from vgc.models import *

def create_test_data():
    testuser = User.objects.create_user(username="testusername", email="test@email.com", password="testpassword")
    testuserprofile = UserProfile.objects.create(user=testuser, picture="/media/cat.jpg")
    testuserprofile.save()

    testuser2 = User.objects.create_user(username="testusername2", email="test2@email.com", password="testpassword2")
    testuserprofile2 = UserProfile.objects.create(user=testuser2, picture="/media/cat.jpg")
    testuserprofile2.save()

    testuser3 = User.objects.create_user(username="testusername3", email="test3@email.com", password="testpassword3")
    testuserprofile3 = UserProfile.objects.create(user=testuser3, picture="/media/cat.jpg")
    testuserprofile3.save()

    Dr_Suvi = [{"name": "Dr. Suvi Anwar",
                "url": "http://masseffect.wikia.com/wiki/Dr._Suvi_Anwar",
                "bio": "Dr. Suvi Anwar is a member of the Nexus’ science team, and holds advanced degrees in astrophysics and molecular biology. In a screening interview, she stated that she was from a “large, rather boisterous family” of five children.",
                "picture": "char_images/DrSuvi.jpg"}]

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
                          "url": "http://masseffect.wikia.com/wiki/Jack",
                          "bio": "Jack, also known as Subject Zero, is a notorious criminal whose crimes include piracy, kidnapping, vandalism and murder. ",
                          "picture": "char_images/Subject_Zero.png"}]

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

    games = {"Mass Effect": {"characters": [Dr_Suvi ,Shepard,JamesVega,KaidanAlenko,Jack_Subject_Zero] , "picture": "game_images/masseffect.jpg" },
            "Halo": {"characters": [John_117, Cortana, Jacob_Keyes, Avery_Johnson, John_Forge], "picture":"game_images/halo.jpg"},
            "Assassin's Creed": {"characters": [Desmond_Miles, Altair, Ezio_Auditore, Edward_Kenway, Lucy_Stillman] , "picture": "game_images/ac.jpg" }
            }

    for games, game_data in games.items():
        c = add_game(games,game_data["picture"])
        for k in game_data["characters"]:
            for p in k:
                add_character(c, p["name"], p["url"], p["bio"],p["picture"])

    testrating1 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Dr. Suvi Anwar"), rating = 100)
    testrating1.save()
    testrating2 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Commander Shepard"), rating=90)
    testrating2.save()
    testrating3 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="James Vega"), rating=80)
    testrating3.save()
    testrating4 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Kaidan Alenko"), rating=70)
    testrating4.save()
    testrating5 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Jack-Subject Zero"), rating=60)
    testrating5.save()
    testrating6 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="John-117"), rating=50)
    testrating6.save()
    testrating7 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Cortana"), rating=40)
    testrating7.save()
    testrating8 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Jacob Keyes"), rating=35)
    testrating8.save()
    testrating9 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Avery Johnson"), rating=30)
    testrating9.save()
    testrating10 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="John Forge"), rating=25)
    testrating10.save()
    testrating11 = Rating.objects.create(user=testuserprofile, character=Character.objects.get(name="Desmond Miles"), rating=20)
    testrating11.save()

    testrating12 = Rating.objects.create(user=testuserprofile2, character=Character.objects.get(name="John Forge"), rating=100)
    testrating12.save()
    testrating13 = Rating.objects.create(user=testuserprofile2, character=Character.objects.get(name="Jack-Subject Zero"), rating=100)
    testrating13.save()

    testlist = ListElement.objects.create(user=testuserprofile, position=1, character=Character.objects.get(name="Dr. Suvi Anwar"))
    testlist.save()

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


class IndexViewTests(TestCase):

    def test_get_index_view_empty(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual([response.context["l"]], ["{}"])

    def test_get_index_view(self):

        create_test_data()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testusername")
        self.assertContains(response, "Dr. Suvi Anwar")
        num_lists = len(response.context["l"])
        self.assertEqual(num_lists, 1)


class RegisterViewTests(TestCase):

    def test_register_view(self):
        response = self.client.get("/vgc/register/")
        self.assertContains(response, "Sign Up Here")

        post_response = self.client.post("/vgc/register/", {"username": "testusername", "email": "test@email.com", "password": "testpassword"}, follow=True)
        self.assertContains(post_response, "Thank you for registering!")


class UserProfileViewTests(TestCase):

    def test_user_profile_view_not_logged_in(self):
        response = self.client.get("/vgc/user_profile/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/user_profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertContains(response, "testusername")
        self.assertContains(response, "test@email.com")


class DeactivateUserViewTests(TestCase):

    def test_deactivate_user_view_not_logged_in(self):
        response = self.client.get("/vgc/deleteaccount/", follow=True)
        self.assertEqual(response.status_code, 200)


    def test_deactivate_user_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/deleteaccount/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete this account?")

        post_response = self.client.post("/vgc/deleteaccount", {"items": "delete"}, follow=True)
        self.assertEqual(post_response.status_code, 200)


class UserLoginViewTest(TestCase):


    def test_user_login_view_incorrect_details(self):
        create_test_data()
        response = self.client.get("/vgc/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login/", {"username": "invalid", "password": "invalid"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertContains(post_response, "Invalid login details provided!")


    def test_user_login_view_not_logged_in(self):
        create_test_data()

        response = self.client.get("/vgc/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login/", {"username": "testusername", "password": "testpassword"}, follow=True)
        self.assertEqual(post_response.status_code, 200)


    def test_user_login_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")

        response = self.client.get("/vgc/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login/", {"username": "testusername", "password": "testpassword"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)


class UserLogoutViewTest(TestCase):

    def test_user_logout_view_not_logged_in(self):
        response = self.client.get("/vgc/logout/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_logout_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")

        response = self.client.get("/vgc/logout/", follow=True)
        self.assertEqual(response.status_code, 200)


class ShowListOfVideogamesViewTest(TestCase):

    def test_show_list_of_videogames_view_empty(self):
        response = self.client.get("/vgc/showlistofgames/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present")

    def test_show_list_of_videogames_view(self):
        create_test_data()
        response = self.client.get("/vgc/showlistofgames/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Halo")


class AllCharactersViewTest(TestCase):

    def test_all_characters_view_empty(self):
        response = self.client.get("/vgc/allcharacters/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no characters present")

    def test_all_characters_view(self):
        create_test_data()
        response = self.client.get("/vgc/allcharacters/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Suvi Anwar")


class TopRatedViewTest(TestCase):

    def test_toprated_view_empty(self):
        response = self.client.get("/vgc/toprated/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no characters present")

    def test_toprated_view(self):
        create_test_data()
        response = self.client.get("/vgc/toprated/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Suvi Anwar")
        self.assertNotContains(response, "Desmond Miles")

        testrating = Rating.objects.create(user=UserProfile.objects.get(user=3),
                                            character=Character.objects.get(name="Altair"), rating=100)
        testrating.save()
        response = self.client.get("/vgc/toprated/")
        self.assertContains(response, "Altair")
        self.assertNotContains(response, "Avery Johnson")



class RecommendationsViewTest(TestCase):

    def test_recommendations_view_not_logged_in(self):
        response = self.client.get("/vgc/recommendations/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")


    def test_recommedations_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername3", password="testpassword3")
        testrating = Rating.objects.create(user=UserProfile.objects.get(user=3),
                                           character=Character.objects.get(name="John Forge"), rating=25)
        testrating.save()

        response = self.client.get("/vgc/recommendations/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Suvi Anwar")
        self.assertNotContains(response, "Jack-Subject Zero")

        testrating.rating = 100
        testrating.save()
        response = self.client.get("/vgc/recommendations/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Dr. Suvi Anwar")
        self.assertContains(response, "Jack-Subject Zero")



class ShowVideogameViewTest(TestCase):

    def test_show_videogame_view_invalid(self):
        response = self.client.get("/vgc/videogame/invalid/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The specified videogame does not exist!")

    def test_show_videogame_view_not_logged_in(self):
        create_test_data()
        response = self.client.get("/vgc/videogame/halo/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cortana")
        self.assertNotContains(response, "Add a Character")

    def test_show_videogame_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/videogame/halo/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cortana")
        self.assertContains(response, "Add a Character")

class ShowCharacterViewTest(TestCase):

    def test_show_character_view_invalid(self):
        response = self.client.get("/vgc/characterpage/invalidcharacter/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The specified character does not exist!")

    def test_show_character_view_not_logged_in(self):
        create_test_data()
        response = self.client.get("/vgc/characterpage/cortana/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cortana, UNSC Artificial intelligence (SN: CTN 0452-9), is a smart artificial intelligence construct.")
        self.assertNotContains(response, "Rate")

    def test_show_character_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/characterpage/cortana/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cortana, UNSC Artificial intelligence (SN: CTN 0452-9), is a smart artificial intelligence construct.")
        self.assertContains(response, "Rate")

class YourTop10ViewTest(TestCase):

    def test_your_top_10_view_not_logged_in(self):
        create_test_data()
        response = self.client.get("/vgc/testuser/yourtop10/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_show_character_view_logged_in_yours(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/testusername/yourtop10/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose Ranked 1")

    def test_show_character_view_logged_in_not_yours(self):
        create_test_data()
        self.client.login(username="testusername2", password="testpassword2")
        response = self.client.get("/vgc/testusername/yourtop10/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Choose Ranked 1")

class AddVideogameViewTest(TestCase):

    def test_add_videogame_view_not_logged_in(self):
        response = self.client.get("/vgc/add_videogame", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_add_videogame_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/add_videogame/")
        self.assertContains(response, "Add a Video Game!")

        post_response = self.client.post("/vgc/add_videogame/", {"name": "test"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(VideoGame.objects.get(name="test"))

class AddCharacterViewTest(TestCase):

    def test_add_character_view_not_logged_in(self):
        create_test_data()
        response = self.client.get("/vgc/videogame/testgame/add_character", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_add_character_view_logged_in(self):
        create_test_data()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/videogame/halo/add_character/")
        self.assertContains(response, "Add a Character to Halo")

        post_response = self.client.post("/vgc/videogame/halo/add_character/", {"name": "test", "url":"http://www.test.com", "bio": "Test", "picture": "cat.jpg"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(Character.objects.get(name="test"))
