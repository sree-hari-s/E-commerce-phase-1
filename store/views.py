from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store') 
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print("hello user")
            return redirect('store')
        else:
            messages.error(request,'Username or password incorrect')
            
    return render(request,'store/login.html') 
    
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            Customer.objects.create(user=user,name=user.username).save()
            login(request,user)
            return redirect('store')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'store/register.html',{'form':form})
    
def logoutUser(request):
    logout(request)
    return redirect('store')

def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0, 'shipping':False }
        cartItems = order['get_cart_items']
        
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)


@login_required()
def products(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0, 'shipping':False }
        cartItems = order['get_cart_items']
        
    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/products.html',context)

@login_required()
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0, 'shipping':False }
        cartItems = order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0, 'shipping':False }
        cartItems = order['get_cart_items']
        
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


@login_required()
def product_detail(request):
    context={}
    return render(request,'store/product-detail.html',context)


@login_required()
def wishlist(request):
    context={}
    return render(request,'store/wishlist.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('productId:',productId)
    
    customer = request.user.customer
    product= Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order,product=product)
    
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1) 
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        print(total)
        print(type(total))
        print(order.get_cart_total)
        print(type(order.get_cart_total))
        if total == order.get_cart_total:
            order.complete= True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in ...')
    return JsonResponse('Payment complete',safe=False)

@login_required
def profile(request):
    context={}
    return render(request,'store/profile.html',context)
