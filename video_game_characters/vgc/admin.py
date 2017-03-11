from django.contrib import admin
from vgc.models import UserProfile, VideoGame, Character

admin.site.register(UserProfile)

# Register your models here.

admin.site.register(Character)

class VideoGameAdmin(admin.ModelAdmin):
    prepopulated_fields =  {'slug':('name',)}

admin.site.register(VideoGame, VideoGameAdmin)