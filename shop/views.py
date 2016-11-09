
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Seller, Customer, Item, Order, OrderItem, Coupon
from .forms import ItemForm


@csrf_protect
def register(request, template='register.html'):

    if request.method == 'GET':
        return render(request, template)

    elif request.method == 'POST':
        username = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if not all([username, password, phone, user_type]):
            data = {
                'error': True,
                'message': "all fields are required"
            }
            return render(request, template, data)

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.email = username
            user.set_password(password)
            user.save()

            if user_type == 'seller':
                s = Seller(user=user, phone=phone)
                s.save()
            elif user_type == 'customer':
                c = Customer(user=user, phone=phone)
                c.save()

            data = {
                'error': False,
                'message': "Successfully registered, visit login page"
            }
            return render(request, template, data)
        else:
            data = {
                'error': True,
                'message': "User already registered, try diff email"
            }
            return render(request, template, data)


@csrf_protect
def signin(request, template='login.html'):

    if request.method == 'GET':
        if request.user.is_authenticated():
            if request.user.seller.first():  # check user type and redirect accordingly
                return HttpResponseRedirect('/seller/')
            return HttpResponseRedirect('/customer/')
        return render(request, template)

    elif request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        if not all([username, password]):
            data = {
                'error': True,
                'message': "both are required"
            }
            return render(request, template, data)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            if request.user.seller.first():  # check user type and redirect accordingly
                return HttpResponseRedirect('/seller/')
            return HttpResponseRedirect('/customer/')
        else:
            data = {
                'error': True,
                'message': "Invalid Username/Password"
            }
            return render(request, template, data)


def signout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user_must_be_seller(user):
    try:
        return user.seller.first()
    except:
        return False


@login_required
@user_passes_test(user_must_be_seller)
@csrf_protect
def seller_add_item(request, template='seller_add_item.html'):
    if request.method == 'GET':
        return render(request, template, {'form': ItemForm()})
    elif request.method == 'POST':
        item_form = ItemForm(request.POST, request.FILES)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.seller = request.user.seller.first()
            item.save()
            data = {
                'error': False,
                'message': 'Saved!'
            }
        else:
            data = {
                'error': True,
                'message': "Please provide some data"
            }
        return render(request, template, data)


@login_required
@user_passes_test(user_must_be_seller)
def seller_view_item(request, template='seller_view_item.html'):
    seller = Seller.objects.get(user=request.user)
    items = seller.item.all()
    return render(request, template, {'items': items})


def user_must_be_customer(user):
    try:
        return user.customer.first()
    except:
        return False


@login_required
@user_passes_test(user_must_be_customer)
def customer_order(request, template='customer_product.html'):
    items = Item.objects.all()   # .exclude(inventory=0)
    return render(request, template, {'items': items})


@login_required
@user_passes_test(user_must_be_customer)
def order_details(request, slug, template='order_details.html'):
    item = get_object_or_404(Item, slug=slug)
    if request.method == 'GET':
        data = {
            'item': item
        }
        return render(request, template, data)

    elif request.method == 'POST':
        addr = request.POST.get('addr')
        item_id = request.POST.get('item')
        coupon = request.POST.get('coupon')

        try:
            coupon = Coupon.objects.get(code=coupon, is_active=True)
        except Coupon.DoesNotExist:
            data = {
                'error': True,
                'message': "Invalid Coupon Code",
                'item': item
            }
            return render(request, template, data)

        item = Item.objects.get(id=item_id)
        item.inventory -= 1
        item.save()

        o = Order(customer=request.user.customer.first(), shipping_detail=addr)
        o.discount = float(coupon.value)
        o.final_price = item.price - float(coupon.value)
        o.save()

        oi = OrderItem(order=o, item=item)
        oi.save()

        response_text = """
        <h3> Order has been placed and order id is: {} </h3>
        <a href='/customer/'> Go back to product listing page </a>
        """.format(o.oid)
        return HttpResponse(response_text)
