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


class ProductsListView(ListView):
  model = models.Product
  form_class = forms.ProductForm
  template_name = 'shop/product.html'

  def get_context_data(self, **kwargs):
    context = super(ProductsListView, self).get_context_data(**kwargs)
    context['form'] = self.form_class()
    return context

  def get_queryset(self):
    return self.model.objects.order_by("category")

  def post(self, request):
    form = self.form_class(request.POST)
    if form.is_valid():
      status = self.model(category=form.cleaned_data['category'],
                          product_name=form.cleaned_data['product_name'],
                          description=form.cleaned_data['description'],
                          price=form.cleaned_data['price'],
                          stock_number=form.cleaned_data['stock_number'],
                          unit= form.cleaned_data['unit'])
      status.save()
      return redirect('index')

class BuyProduct(View):
  template_name = 'shop/buy_product.html'
  form_class = forms.Selector
  model = models.Product

  def get(self, request,pk):
    product = models.Product.objects.get(pk=pk)
    context = {
        'form': forms.Selector(),
        'product': product
    }
    return render(request, 'shop/buy_product.html', context)

  def post(self, request,pk):
    form = self.form_class(request.POST)
    if form.is_valid():
      quantity =form.cleaned_data['quantity']
      product = models.Product.objects.filter(pk=pk)
      product.update(stock_number=F('stock_number') - quantity)
      unit =product.values_list("unit", flat=True)[0] #extragem unitatea de masura a produsului


    return redirect('index')

def deleteProduct(request,primary_key):
  if request.method == 'GET':
    models.Product.objects.filter(pk=primary_key).delete()
    return redirect('index')

def pp(request):
  return render(request,'shop/PP.html')

def login_view(request):
    context = {}
    if request.method == 'GET':
        form = forms.LoginForm()
    elif request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request=request,
                      user=user)
                return redirect('index')
            else:
                context['error_message'] = 'Wrong username or password!'
    context['form'] = form
    return render(request, 'shop/login.html', context)

def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('index')
