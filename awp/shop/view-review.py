from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.list import View
from django.db.models import F
from django.contrib import messages

from . import models
from . import forms


class ReviewListView(ListView):
  model = models.Review
  form_class = forms.ReviewForm
  template_name = 'shop/review-list.html'

  def get_context_data(self, **kwargs):
    context = super(ReviewListView, self).get_context_data(**kwargs)
    context['form'] = self.form_class()
    return context

  def get_queryset(self):
    return self.model.objects.order_by("date")

  def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
      status = self.model(product_name = form.cleaned_data['product_name'],
                          client_name = form.cleaned_data['client_name'],
                          comment = form.cleaned_data['comment'],
                          date = form.cleaned_data['date']
                          )
      status.save()
      return redirect('index')

  def get(self, request, pk):
    review = models.Review.objects.get(pk=pk)
    context = {
        'form': forms.Selector(),
        'review': review
    }
    return render(request, 'shop/buy_product.html', context)

  def post(self, request, pk):
    form = self.form_class(request.POST)
    if form.is_valid():
      comment = form.cleaned_data['comment']
      review = models.Review.objects.filter(pk=pk)

    return redirect('index')

def deleteProduct(request, primary_key):
  if request.method == 'GET':
    models.Review.objects.filter(pk=primary_key).delete()
    return redirect('index')