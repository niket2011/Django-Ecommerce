from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from .models import OrderItem
from .forms import OrderCreateForm
# Create your views here.
def home_view(request,*args,**kwargs):
    return render(request,'home.html',{})


def product_create_view(request):
    form=ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=ProductForm()
    context={
        'form':form
    }
    return render(request,"product/product_create.html",context)

def product_delete_view(request,id):
    obj=get_object_or_404(Product, id=id)
    if request.method=='POST':
        obj.delete()
        redirect('../../')
    context={
        'object':obj
    }
    return render(request,'product/product_delete.html',context)

def product_list_view(request):
    queryset=Product.objects.all()
    context={
        'object_list':queryset
    }
    return render(request,'product/product_list.html',context)


def product_detail_view(request,id):
    obj=get_object_or_404(Product,id=id)
    cart_product_form = CartAddProductForm()
    context={
        'object':obj,
        'cart_product_form': cart_product_form
    }
    return render(request,'product/product_detail.html', context)




class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def contact_page(request):
        contact_form = ContactForm(request.POST or None)
        context = {
            "title": "Contact",
            "content": " Welcome to the contact page.",
            "form": contact_form,
        }
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
            if request.is_ajax():
                return JsonResponse({"message": "Thank you for your submission"})

        if contact_form.errors:
            errors = contact_form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')

        # if request.method == "POST":
        #     #print(request.POST)
        #     print(request.POST.get('fullname'))
        #     print(request.POST.get('email'))
        #     print(request.POST.get('content'))
        return render(request, "contact/view.html", context)
def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "about.html", context)


@require_POST
def cart_add(request,id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('Product:cart-detail')


def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('Product:cart-detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
        return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'form': form})


def search_list(request):
    object_list = Product.objects.all()
    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(name__icontains=query)

        return render(request, 'product/product_list.html', {'object_list': object_list})
