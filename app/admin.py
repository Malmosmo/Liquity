from django.contrib import admin

from .models import Beer, Drink, Group

admin.site.register(Group)
admin.site.register(Beer)
admin.site.register(Drink)
