from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from vgc.models import *

def create_test_user():
    testuser = User.objects.create_user(username="testusername", email="test@email.com", password="testpassword")
    testuserprofile = UserProfile.objects.create(user=testuser, picture="/media/cat.jpg")
    testuserprofile.save()

    testgame = VideoGame.objects.create(name="testgame", picture = "media/game_images/halo.jpg")
    testgame.save()
    testcharacter1 = Character.objects.create(videogame=testgame, name="testcharactername", url="google.com",
                                              bio="test bio", picture = "media/char_images/Cortana.jpg")
    testcharacter1.save()

    testrating = Rating.objects.create(user=testuserprofile, character = testcharacter1, rating = 100)
    testrating.save()

    testlist = ListElement.objects.create(user=testuserprofile, position=1, character=testcharacter1)
    testlist.save()

#done
class IndexViewTests(TestCase):

    def test_get_index_view_empty(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual([response.context["l"]], ["{}"])

    def test_get_index_view(self):

        create_test_user()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testusername")
        self.assertContains(response, "testcharactername")
        num_lists = len(response.context["l"])
        self.assertEqual(num_lists, 1)

#in progress
class RegisterViewTests(TestCase):

    def test_register_view(self):
        response = self.client.get("/vgc/register/")

#done
class UserProfileViewTests(TestCase):

    def test_user_profile_view_not_logged_in(self):
        response = self.client.get("/vgc/user_profile/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/user_profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertContains(response, "testusername")
        self.assertContains(response, "test@email.com")

#done
class DeactivateUserViewTests(TestCase):

    def test_deactivate_user_view_not_logged_in(self):
        response = self.client.get("/vgc/deleteaccount/", follow=True)
        self.assertEqual(response.status_code, 200)


    def test_deactivate_user_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/deleteaccount/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete this account?")

        post_response = self.client.post("/vgc/deleteaccount", {"items": "delete"}, follow=True)
        self.assertEqual(post_response.status_code, 200)

#done
class UserLoginViewTest(TestCase):


    def test_user_login_view_incorrect_details(self):
        create_test_user()
        response = self.client.get("/vgc/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login", {"username": "invalid", "password": "invalid"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)


    def test_user_login_view_not_logged_in(self):
        create_test_user()

        response = self.client.get("/vgc/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login", {"username": "testusername", "password": "testpassword"}, follow=True)
        self.assertEqual(post_response.status_code, 200)


    def test_user_login_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")

        response = self.client.get("/vgc/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please sign in")

        post_response = self.client.post("/vgc/login", {"username": "testusername", "password": "testpassword"},
                                         follow=True)
        self.assertEqual(post_response.status_code, 200)

#done
class UserLogoutViewTest(TestCase):

    def test_user_logout_view_not_logged_in(self):
        response = self.client.get("/vgc/logout/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_logout_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")

        response = self.client.get("/vgc/logout/", follow=True)
        self.assertEqual(response.status_code, 200)

#done
class ShowListOfVideogamesViewTest(TestCase):

    def test_show_list_of_videogames_view_empty(self):
        response = self.client.get("/vgc/showlistofgames/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no games present")

    def test_show_list_of_videogames_view(self):
        create_test_user()
        response = self.client.get("/vgc/showlistofgames/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testgame")

#done
class AllCharactersViewTest(TestCase):

    def test_all_characters_view_empty(self):
        response = self.client.get("/vgc/allcharacters/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no characters present")

    def test_all_characters_view(self):
        create_test_user()
        response = self.client.get("/vgc/allcharacters/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testcharacter")

#in progress
class TopRatedViewTest(TestCase):

    def test_toprated_view_empty(self):
        response = self.client.get("/vgc/toprated/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no characters present")

    def test_toprated_view(self):
        response = self.client.get("/vgc/toprated/")

#in progress
class RecommendationsViewTest(TestCase):

    def test_recommendations_view_not_logged_in(self):
        response = self.client.get("/vgc/recommendations/", follow=True)
        self.assertEqual(response.status_code, 200)

    '''
    def test_recommedations_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")

        response = self.client.get("/vgc/recommendations/")
    '''

#in progress
class ShowVideogameViewTest(TestCase):

    def test_show_videogame_view_invalid(self):
        response = self.client.get("/vgc/videogame/(?P<videogame_name_slug>[\w\-]+)")

    def test_show_videogame_view_not_logged_in(self):
        response = self.client.get("/vgc/videogame/(?P<videogame_name_slug>[\w\-]+)")

    def test_show_videogame_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/videogame/(?P<videogame_name_slug>[\w\-]+)")

#in progress
class ShowCharacterViewTest(TestCase):

    def test_show_character_view_invalid(self):
        response = self.client.get("/vgc/characterpage/invalidcharacter")

    def test_show_character_view_not_logged_in(self):
        response = self.client.get("/vgc/characterpage/(?P<character_name_slug>[\w\-]+)")

    def test_show_character_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/characterpage/(?P<character_name_slug>[\w\-]+)")

#in progress
class YourTop10ViewTest(TestCase):

    def test_your_top_10_view_not_logged_in(self):
        response = self.client.get("/vgc/invaliduser/yourtop10")

    def test_show_character_view_logged_in(self):
        response = self.client.get("/vgc/(?P<user>[\w\-]+)/yourtop10")

#in progress
class AddVideogameViewTest(TestCase):

    def test_add_videogame_view_not_logged_in(self):
        response = self.client.get("/vgc/add_videogame", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_videogame_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/add_videogame")

#in progress
class AddCharacterViewTest(TestCase):

    def test_add_character_view_not_logged_in(self):
        create_test_user()
        response = self.client.get("/vgc/videogame/testgame/add_character", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_character_view_logged_in(self):
        create_test_user()
        self.client.login(username="testusername", password="testpassword")
        response = self.client.get("/vgc/videogame/(?P<videogame_name_slug>[\w\-]+)/add_character")
