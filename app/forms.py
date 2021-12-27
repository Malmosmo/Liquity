from django import forms

from .models import Drink
from django.utils.translation import gettext_lazy as _


class GroupCreateForm(forms.Form):
    name = forms.CharField(label=_("Group Name"), max_length=100)


class GroupRenameForm(forms.Form):
    name = forms.CharField(label=_("New Group Name"), max_length=100)


class DrinkCreateForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'image']


class DrinkEntryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.DateInput(attrs={"type": "time"}))
    drink = forms.CharField()
    volume = forms.FloatField(label=_("Volume (in Liters)"), min_value=0.0, max_value=100.0, widget=forms.NumberInput(attrs={"step": "0.01", "value": "0.5"}))
    count = forms.IntegerField(min_value=1, max_value=99)
