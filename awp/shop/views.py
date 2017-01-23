from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.list import View
from django.db.models import F

from . import models
from . import forms

def create_client_cart(user):
  try:
    client = models.Client.objects.get(user=user)
  except models.Client.DoesNotExist:
    client = models.Client(user=user)
    client.save()
  try:
    cart = models.MyShoppingCart.objects.get(client=client)
  except models.MyShoppingCart.DoesNotExist:
    cart =models.MyShoppingCart(client=client)
    cart.save()

def get_cart(user):
  client = models.Client.objects.get(user=user)
  return models.MyShoppingCart.objects.get(client=client)

def add_item_to_cart(user,product,quantity):
    cartItem=models.ShoppingCartItem(cart=get_cart(user),product=product,quantity=quantity)
    cartItem.save()


class ProductsListView(LoginRequiredMixin, ListView):
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
    else:
      context = {
        'form': form,
        'product_list':self.get_queryset(),
      }
      return render(request, self.template_name, context)

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
    product = models.Product.objects.filter(pk=pk)
    if form.is_valid():
      quantity =form.cleaned_data['quantity']
      currentQuantity = product.values_list("stock_number", flat=True)[0]
      unitate = product.values_list("unit", flat=True)[0]
      if currentQuantity >= quantity:
        if unitate == 'Units' and quantity.is_integer():
         product.update(stock_number=F('stock_number') - quantity)
         add_item_to_cart(request.user,product.first(),quantity)
        elif product.values_list("unit", flat=True)[0] != 'Units':
          product.update(stock_number=F('stock_number') - quantity)
          add_item_to_cart(request.user, product.first(), quantity)

      return redirect('index')


class UpdateProduct(View):
  template_name = 'shop/update_product.html'
  form_class = forms.ProductForm
  model = models.Product


  def get(self, request,pk):
    product = models.Product.objects.filter(pk=pk)
    formular = forms.ProductForm()
    formular.fields["category"].initial = product.values_list("category", flat=True)[0]
    formular.fields["product_name"].initial = product.values_list("product_name", flat=True)[0]
    formular.fields["description"].initial = product.values_list("description", flat=True)[0]
    formular.fields["price"].initial = product.values_list("price", flat=True)[0]
    formular.fields["stock_number"].initial = product.values_list("stock_number", flat=True)[0]
    formular.fields["unit"].initial = product.values_list("unit", flat=True)[0]

    context = {
        'form': formular,
        'product': product
    }
    return render(request, 'shop/update_product.html', context)

  def post(self, request,pk):
    form = self.form_class(request.POST)
    if form.is_valid():
      product = models.Product.objects.filter(pk=pk)
      product.update(category=form.cleaned_data['category'])
      product.update(product_name=form.cleaned_data['product_name'])
      product.update(description=form.cleaned_data['description'])
      product.update(price=form.cleaned_data['price'])
      product.update(stock_number=form.cleaned_data['stock_number'])
      product.update(unit=form.cleaned_data['unit'])

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
                create_client_cart(user)
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


def display_cart_items(request):
  cart = get_cart(request.user)
  items = models.ShoppingCartItem.objects.filter(cart=cart)
  context={"items":items}
  return render(request, 'shop/cart.html', context)




