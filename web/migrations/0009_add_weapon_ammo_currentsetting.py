# Generated by Django 4.2.11 on 2024-06-30 20:00

from django.db import migrations, models

def add_objects(apps, schema_editor):
    Weapon = apps.get_model('web', 'Weapon')
    Ammo = apps.get_model('web', 'Ammo')
    CurrentSetting = apps.get_model('web', 'CurrentSetting')
    

    if Weapon.objects.count() == 0:
        Weapon.objects.create(
            name="Default",
            sight_height=5,
            zero_distance=100,
            twist=12,
            zero_look_angle=0
        )

    if Ammo.objects.count() == 0:
        Ammo.objects.create(
            name="Default",
            length=1,
            mv=800,
            value=0.5,
            drag_table='G1',
            weight=100,
            diameter=0.5
        )

    if CurrentSetting.objects.count() == 0:
        CurrentSetting.objects.create(
            weapon=Weapon.objects.first(),
            ammo=Ammo.objects.first(),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_currentsetting_laser'),
    ]

    operations = [
        migrations.RunPython(add_objects)
    ]
