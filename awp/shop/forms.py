from django import forms
import datetime

class ProductForm(forms.Form):
  category = forms.CharField(label="Category", widget=forms.Textarea)
  product_name = forms.CharField(label="Name", widget=forms.Textarea)
  description = forms.CharField(label="Description", widget=forms.Textarea)
  price = forms.FloatField(label="Price", min_value=0.1)
  stock_number = forms.FloatField(label="Stock Number", min_value=0.1)
  unit=forms.ChoiceField(label="Unit",choices=[('Units', 'Units'),('L', 'L'),('Kg', 'kg')])


class Selector(forms.Form):
  #quantity = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
  quantity= forms.IntegerField(label="Buy quantity",min_value=0)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class ReviewForm(forms.Form):
  product_name = forms.CharField(label = "Category", widget = forms.Textarea)
  client_name = forms.CharField(label = "Name", widget = forms.Textarea)
  comment = forms.CharField(label = "Description", widget=forms.Textarea)
  date = forms.DateField(initial = datetime.date.today)