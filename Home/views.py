from .models import Product, Category, Blog, ProductType
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
from .models import Contact
from decimal import Decimal
from django.urls import reverse
from .models import Order, OrderItem, CartItem



# Create your views here.
product = Product.objects.all()
product_type = ProductType.objects.all()
categories = Category.objects.all()

navBar = [
        {
            'title': 'Home',
            'link': '/',
            'class': ''
        },
        {
            'title': 'Shop',
            'link': '/shop/',
            'class':''
        },
        {
            'title': 'Features',
            'link': '/features/',
            'class': ''
        },
        # {
        #     'title': 'Blog',
        #     'link': '/blog/',
        #     'class': ''
        # },
        {
            'title': 'About',
            'link': '/about/',
            'class': ''
        },
        {
            'title': 'Contact',
            'link': '/contact/',
            'class': ''
        },
    ]

def home(request):
    cart = request.session.get('cart', {})
    cart_count = request.session.get('cart_count', 0)  # Get cart count from session
    paginator = Paginator(product, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {
        'product': page_obj,
        'categories': categories,
        'navbar': navBar,
        'cart': cart,
        'cart_count': cart_count,  # Pass cart_count to template
        'product_type': product_type,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()  # Fetch all related images for the product
    cart = request.session.get('cart', {})
    cart_count = request.session.get('cart_count', 0)
      # Safely retrieve 'cart' from session

    # Optional: Debugging prints can be removed in production
    print('Cart exists:', 'cart' in request.session)
    print(cart)

    return render(request, 'product_detail.html', {
        'product': product,
        'images': images,  # Pass the queryset of images
        'navbar': navBar,
        'cart': cart,  # Pass the cart to the template if needed
        'cart_count': cart_count,  # Pass cart_count to template

    })

def about(request):
    cart_count = request.session.get('cart_count', 0)
    return render(request, 'about.html' ,{
        'navbar':navBar,
        'product': product,
        'cart_count': cart_count,  # Pass cart_count to template
        })

def contact(request):
    cart_count = request.session.get('cart_count', 0)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, "Your message has been sent!")
            return redirect('contact')  # Redirect to avoid resubmission on page refresh
        else:
            messages.error(request, "There was an error in your form. Please correct it.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'navbar': navBar,
        'form': form,
        'cart_count': cart_count,  # Pass cart_count to template

    })

def shop(request):
    category_slug = request.GET.get('category', 'all')
    page_number = request.GET.get('page')
    cart_count = request.session.get('cart_count', 0)

    if category_slug == 'all':
        products = Product.objects.all()
    else:
        # Ensure you're filtering by slug
        products = Product.objects.filter(category__slug__iexact=category_slug)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'product': page_obj,
        'categories': Category.objects.all(),
        'navbar': navBar,
        'selected_category': category_slug,
        'cart_count': cart_count,  # Pass cart_count to template
    })

def blog(request):
    cart_count = request.session.get('cart_count', 0)
    blog = Blog.objects.all().order_by('-date_posted')
    return render(request, 'blog.html', {
        'navbar':navBar,
        'blogs': blog,
        'cart_count': cart_count,  # Pass cart_count to template
        })

def blog_detail(request, blog_id):
    cart_count = request.session.get('cart_count', 0)
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'navbar': navBar,
        'cart_count': cart_count,  # Pass cart_count to template
    })

def features(request):
    # Get the top 5 products by sales count (or however many you want)
    hot_sales_products = Product.objects.order_by('-sales_count')[:5]
    cart_count = request.session.get('cart_count', 0)

    return render(request, 'features.html', {
        'hot_sales_products': hot_sales_products,
        'navbar':navBar,
        'product': product,
        'cart_count': cart_count,  # Pass cart_count to template
    })


def cart(request):
    cart = request.session.get('cart', {})
    cart_count = request.session.get('cart_count', 0)
    cart_items = []
    subtotal = Decimal(0)

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, id=item_id)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
        subtotal += total_price

    shipping = Decimal(350)
    total = subtotal + shipping

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        return redirect('order_confirmation')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'navbar': navBar,
        'cart_count': cart_count,
    }
    return render(request, 'cart.html', context)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    request.session['cart_count'] = CartItem.objects.aggregate(sum('quantity'))['quantity__sum'] or 0
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session['cart_count'] = sum(cart.values())  # Update total item count
    return redirect('cart')

def confirm_order(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        cell_number = request.POST['cell_number']
        address = request.POST['address']
        
        order = Order.objects.create(
            full_name=full_name,
            cell_number=cell_number,
            address=address,
            shipping=Decimal('100.00')
        )

        cart_items = CartItem.objects.all()
        subtotal = 0
        for item in cart_items:
            order_item = OrderItem.objects.create(
                product=item.product,
                quantity=item.quantity
            )
            order.order_items.add(order_item)
            subtotal += item.total_price()

        order.subtotal = subtotal
        order.total = order.subtotal + order.shipping
        order.save()

        CartItem.objects.all().delete()
        request.session['cart'] = {}
        request.session['cart_count'] = 0

        return redirect('thank_you')
    return redirect('cart')


def thank_you(request):
    return render(request, 'thank_you.html')