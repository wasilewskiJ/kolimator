from turtle import width
from django.db import models

class Weapon(models.Model):
    name = models.CharField(max_length=255)

    sight_height = models.FloatField(help_text="Height of the sight above the bore axis (centimeters)")
    zero_distance = models.FloatField(help_text="Distance at which the weapon is zeroed (meters)")
    twist = models.FloatField(help_text="Twist rate of the barrel (inches)")
    zero_look_angle = models.FloatField(help_text="Angle of the sight line relative to the bore axis (degrees)")

    def __str__(self):
        return self.name
    
class Ammo(models.Model):
    name = models.CharField(max_length=255)

    length = models.FloatField(help_text="Length of the projectile (inches)")
    mv = models.FloatField(help_text="Muzzle velocity (m/s)")

    # drag model
    value = models.FloatField(help_text="Drag coefficient")
    class DragTableChoices(models.TextChoices):
        G1 = 'G1', 'G1'
        G7 = 'G7', 'G7'
        G2 = 'G2', 'G2'
        G5 = 'G5', 'G5'
        G6 = 'G6', 'G6'
        G8 = 'G8', 'G8'
        GI = 'GI', 'GI'
        GS = 'GS', 'GS'
        
    drag_table = models.TextField(help_text="Drag table", choices=DragTableChoices.choices)
    weight = models.FloatField(help_text="Weight of the projectile (grains)")
    diameter = models.FloatField(help_text="Diameter of the projectile (inches)")

    weapons = models.ManyToManyField(Weapon, related_name='ammo')

    def __str__(self):
        return self.name

class Crosshair(models.Model):
    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to='crosshairs/')

    def __str__(self):
        return self.name
class CurrentSetting(models.Model):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    ammo = models.ForeignKey(Ammo, on_delete=models.CASCADE)
    distance = models.FloatField(default=100)

    color_r = models.IntegerField(default=255)
    color_g = models.IntegerField(default=255)
    color_b = models.IntegerField(default=255)

    mode = models.TextField(choices=[('manual', 'MANUAL'), ('slow', 'AUTO: SLOW'), ('fast', 'AUTO: FAST')], default='manual', verbose_name='Rangefinder mode')

    plot = models.BooleanField(default=True)

    crosshair = models.ForeignKey(Crosshair, on_delete=models.SET_NULL, null=True, blank=True)
    crosshair_size = models.IntegerField(default=40)
    crosshair_width = models.IntegerField(default=8)

    laser = models.BooleanField(default=False)



    
