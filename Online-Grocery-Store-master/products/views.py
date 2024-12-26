from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Offer, Order, Categorie
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}
    # products = Product.objects.all()
    categories = Categorie.objects.all()
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        if categorie_id == "10":
            print("yash")
            products = Product.objects.all()
        else:
            products = Product.get_all_products_by_categorieid(categorie_id)
    else:
        products = Product.objects.all()
    data = {}
    data['products'] = products
    data['categories'] = categories
    # return HttpResponse('Hello, Welcome to the project')
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    if product is not None:
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
    return render(request, 'index.html', data)


def cart(request):
    if request.method == 'POST':
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})
    else:
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})


def thank_you(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user_id = request.session.get('user_id')  # Get user_id from session
        carts = request.session.get('cart')  # Get cart from session
        products = Product.get_products_by_id(list(carts.keys()))  # Get products in the cart
        
        print(address, phone, user_id, carts, products)
        if not user_id:
            # If user_id is not found in session, redirect to login page
            messages.error(request, 'User not logged in. Please log in to continue.')
            return redirect('/login')

        if len(phone) == 10:
            if phone[0] in "7896":  # Valid phone number check
                # Fetch the user object from the database
                user = User.objects.get(id=user_id)

                # Loop through products and create orders
                for product in products:
                    order = Order(user=user, product=product, price=product.price,
                                  quantity=carts.get(str(product.id)), address=address, phone=phone)
                    order.save()  # Save the order object after ensuring 'user' is saved
                    # Assuming `place_order()` method is being used elsewhere to handle order-related logic.
                
                # Clear the cart session after placing the order
                request.session['cart'] = {}
                
                # Render the thank you page
                return render(request, 'Thank you.html')
            else:
                messages.error(request, 'Invalid Phone number')
                return redirect('/products/cart')
        else:
            messages.error(request, 'Phone no should have 10 digits')
            return redirect('/products/cart')

    else:
        return redirect('/')
