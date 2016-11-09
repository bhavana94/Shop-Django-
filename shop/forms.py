from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    name = forms.CharField(max_length=255)
    price = forms.FloatField()
    inventory = forms.IntegerField()
    image = forms.ImageField()

    class Meta:
        model = Item
        fields = ['name', 'price', 'inventory', 'image']
