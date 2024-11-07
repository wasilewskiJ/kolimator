from django.contrib import admin

from .models import Weapon, Ammo, Crosshair

admin.site.register(Weapon)
admin.site.register(Ammo)
admin.site.register(Crosshair)