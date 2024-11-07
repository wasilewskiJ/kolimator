from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from py_ballisticcalc import Velocity, Distance, Angular
from py_ballisticcalc import DragModel, TableG7, TableG1, TableG2, TableG5, TableG6, TableG8, TableGI, TableGS
from py_ballisticcalc import Ammo, Unit, PreferredUnits
from py_ballisticcalc import Weapon, Shot, Calculator
from . import models
from django import forms
import json
import os

from .get_distance import get_distance

import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PreferredUnits.distance = Unit.Meter
PreferredUnits.velocity = Unit.MPS
PreferredUnits.drop = Unit.Meter
PreferredUnits.sight_height = Unit.Centimeter
PreferredUnits.temperature = Unit.Celsius

def set_laser(on=True):
    print(f"Setting laser to {on}")
    pass

coordinates_file = "/home/kolimator/coordinates.json"
center_x, center_y = 1300, 425

drag_tables = {
    'G1': TableG1,
    'G7': TableG7,
    'G2': TableG2,
    'G5': TableG5,
    'G6': TableG6,
    'G8': TableG8,
    'GI': TableGI,
    'GS': TableGS,
}

class ShotForm(forms.ModelForm):
    class Meta:
        model = models.CurrentSetting
        fields = ['weapon', 'ammo', 'distance', 'mode', 'laser', 'plot', 'crosshair', 'crosshair_size', 'crosshair_width']
    
    def __init__(self, *args, **kwargs):
        super(ShotForm, self).__init__(*args, **kwargs)
        self.fields['crosshair'].empty_label = 'Default'

    
def read_coordinates():
    if os.path.isfile(coordinates_file):
        with open(coordinates_file, 'r') as file:
            data = json.load(file)
            print(f"Read coordinates: {data}")  # Debugging output
            return data.get('x', 0), data.get('y', 0)
    return 0, 0

def write_coordinates(x, y, settings_instance):
    data = {
        "x": x,
        "y": y,
        "crosshair": {
            "file": settings_instance.crosshair.file.path if settings_instance.crosshair else "",
            "r": settings_instance.color_r,
            "g": settings_instance.color_g,
            "b": settings_instance.color_b,
            "width": 4,
            "size": 40
        },
        "distance": settings_instance.distance,
    }
    
    if not os.path.isfile(coordinates_file):
        print(data)
        return
    
    with open(coordinates_file, 'w') as file:
        json.dump(data, file)
        print(f"Wrote coordinates: {data}")  # Debugging output

def shot_view(request):
    if request.method == 'POST':
        form = ShotForm(request.POST, instance=models.CurrentSetting.objects.first())
    else:
        form = ShotForm(instance=models.CurrentSetting.objects.first())

    info = None
    plot = None
    err = None

    weapon_model = form.instance.weapon
    ammo_model = form.instance.ammo
    distance = form.instance.distance

    if form.is_valid():
        weapon_model = form.cleaned_data['weapon']
        ammo_model = form.cleaned_data['ammo']
        distance = form.cleaned_data['distance']

        rangefinder_mode = form.cleaned_data['mode']

        if rangefinder_mode == 'slow':
            distance_read, err = get_distance()
            if distance_read:
                distance = distance_read
                form.data._mutable = True
                form.data['distance'] = distance_read
        elif rangefinder_mode == 'fast':
            distance_read, err = get_distance(fast = True)
            if distance_read:
                distance = distance_read
                form.data._mutable = True
                form.data['distance'] = distance_read

        color = request.POST.get('color')
        if color:
            color = color.strip('rgb(').strip(')').split(',')
            form.instance.color_r = color[0]
            form.instance.color_g = color[1]
            form.instance.color_b = color[2]    

        form.save()

        if form.cleaned_data['laser']:
            set_laser(True)
        else:
            set_laser(False)

    if weapon_model and ammo_model:

        dm = DragModel(
            bc=ammo_model.value,
            drag_table=drag_tables[ammo_model.drag_table],
            weight=ammo_model.weight,
            diameter=ammo_model.diameter,
            length=ammo_model.length,
        )

        ammo = Ammo(
            dm=dm,
            mv=Velocity(ammo_model.mv, Velocity.MPS),
        )

        weapon = Weapon(
            sight_height=weapon_model.sight_height,
            twist=weapon_model.twist,
            zero_elevation=weapon_model.zero_look_angle,
        )

        calc = Calculator()
        shot = Shot(
            weapon=weapon,
            ammo=ammo,
        )

        calc.set_weapon_zero(shot, Distance.Meter(weapon_model.zero_distance))

        calc2 = Calculator()
        barrel_elevation = calc2.barrel_elevation_for_target(shot, Distance.Meter(distance))
        shot.relative_angle = Angular.MOA(barrel_elevation.get_in(Angular.MOA) - weapon.zero_elevation.get_in(Angular.MOA))
        moa_shift = round(shot.relative_angle >> Angular.MOA, 2)
        info = f"{moa_shift} MOA UP"

        # Calculate pixel shift
        pixel_shift = moa_shift / 0.3448

        # Update coordinates
        new_x = center_x + pixel_shift
        write_coordinates(new_x, center_y, form.instance)
        
        if form.instance.plot:

            shot_result = calc2.fire(
                shot=shot,
                trajectory_range=Distance.Meter(distance*1.5),
                extra_data=True
            )

            ax = shot_result.plot()
            ax.set_facecolor((.9, .9, .9, .8))
            ax.get_figure().set_facecolor((0, 0, 0, 0))

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            

    return render(request, 'web/shot.html', {
        'form': form, 'plot': plot, 'info': info, 'weapon': weapon_model, 'ammo': ammo_model, 'err': err,
        'color_r': form.instance.color_r, 'color_g': form.instance.color_g, 'color_b': form.instance.color_b,
        })

