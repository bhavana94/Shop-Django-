from django import forms
from .models import Seller, Item, Order


class ItemForm(forms.ModelForm):

	name = forms.CharField(max_length=255)
	price = forms.FloatField()
	inventory = forms.IntegerField()
	image = forms.ImageField()

	class Meta:
	    model = Item
	    fields = ['name', 'price', 'inventory', 'image']


class OrderForm(forms.ModelForm):

	discount = forms.FloatField()
	final_price = forms.FloatField()
	shipping_detail = forms.CharField(max_length=50, widget = forms.Textarea)

	class Meta:
		model = Order
		fields = ['id', 'discount', 'final_price', 'shipping_detail']
