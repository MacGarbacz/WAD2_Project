from django.conf.urls import url
from vgc import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^showlistofgames/$',views.show_listofvideogame,name='show_list_of_games'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^user_profile/$',views.user_profile,name='user_profile'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^characterpage/(?P<character_name_slug>[\w\-]+)/$', views.show_character, name='show_character'),
    url(r'^(?P<user>[\w\-]+)/yourtop10/$',views.your_top_10, name='your_top_10'),
    url(r'^videogame/(?P<videogame_name_slug>[\w\-]+)/$',views.show_videogame, name='show_videogame'),
    url(r'^add_videogame/$', views.add_videogame, name='add_videogame'),
    url(r'^videogame/(?P<videogame_name_slug>[\w\-]+)/add_character/$',
        views.add_character, name='add_character'),
    url(r'^allcharacters/$', views.allcharacters, name='all_characters'),
]