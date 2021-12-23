from django.contrib import admin

from .models import Drink, DrinkEntry, Group

admin.site.register(Group)
admin.site.register(Drink)
admin.site.register(DrinkEntry)
