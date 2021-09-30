from .models import Beer, Drink
from django import forms


class GroupCreateForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)


class GroupRenameForm(forms.Form):
    name = forms.CharField(label="New Group Name", max_length=100)


class BeerCreateForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ['name', 'image']


class DrinkCreateForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['date', 'beer', 'count']


class DrinkForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.DateInput(attrs={"type": "time"}))
    beer = forms.CharField()
    count = forms.IntegerField(min_value=1, max_value=99)
