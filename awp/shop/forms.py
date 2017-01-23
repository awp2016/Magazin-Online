from django import forms
import datetime


class ProductForm(forms.Form):
  category = forms.CharField(label="Category", widget=forms.Textarea)
  product_name = forms.CharField(label="Name", widget=forms.Textarea)
  description = forms.CharField(label="Description", widget=forms.Textarea)
  price = forms.FloatField(label="Price", min_value=0.1)
  stock_number = forms.FloatField(label="Stock Number", min_value=0.1)
  unit=forms.ChoiceField(label="Unit",choices=[('Units', 'Units'),('L', 'L'),('Kg', 'kg')])

  def clean(self):
    cleaned_data = super(ProductForm, self).clean()
    stock = cleaned_data.get("stock_number")
    unit = cleaned_data.get("unit")

    if stock and unit:
      # Only do something if both fields are valid so far.
      if unit == 'Units' and stock%10 != 0:
        raise forms.ValidationError(
          "For unit 'Units' enter a whole number"
        )


class Selector(forms.Form):
  #quantity = forms.ChoiceField(choices=[(x, x) for x in range(1, 100)])
  quantity= forms.FloatField(label="Buy quantity",min_value=0)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
