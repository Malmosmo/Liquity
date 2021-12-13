from django import forms

from .models import Beer


class GroupCreateForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)


class GroupRenameForm(forms.Form):
    name = forms.CharField(label="New Group Name", max_length=100)


class BeerCreateForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ['name', 'image']


# class DrinkCreateForm(forms.ModelForm):
#     class Meta:
#         model = Drink
#         fields = ['date', 'beer', 'count', 'volume']


class DrinkForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.DateInput(attrs={"type": "time"}))
    beer = forms.CharField()
    volume = forms.FloatField(label="Volume (in Liters)", min_value=0.0, max_value=100.0, widget=forms.NumberInput(attrs={"step": "0.01", "value": "0.5"}))
    # amount = forms.FloatField(label="Volume", min_value=0)
    # unit = forms.ChoiceField(label="Unit", choices=(("l", "l"), ("ml", "ml")))
    count = forms.IntegerField(min_value=1, max_value=99)
