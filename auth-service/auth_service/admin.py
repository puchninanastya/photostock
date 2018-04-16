from django.contrib import admin

from .models import UserProfile, UserToken, AppToken

admin.site.register(UserProfile)
admin.site.register(UserToken)
admin.site.register(AppToken)