from django import forms
import datetime


class ReviewForm(forms.Form):
  product_name = forms.CharField(label = "Category", widget = forms.Textarea)
  client_name = forms.CharField(label = "Name", widget = forms.Textarea)
  comment = forms.CharField(label = "Description", widget=forms.Textarea)
  date = forms.DateField(initial = datetime.date.today)