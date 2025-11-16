from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# Helper function – get cart from session
def get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)

    product_id = str(product.id)
    cart[product_id] = cart.get(product_id, 0) + 1  # increase quantity
    save_cart(request, cart)

    return redirect('store:cart_view')


def cart_remove(request, pk):
    cart = get_cart(request)
    product_id = str(pk)

    if product_id in cart:
        del cart[product_id]
        save_cart(request, cart)

    return redirect('store:cart_view')


def cart_view(request):
    cart = get_cart(request)
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    cart = get_cart(request)

    if request.method == 'POST':
        # In a real app you’d process payment, save order etc.
        # For now we just clear the cart and show a success message.
        request.session['cart'] = {}
        request.session.modified = True
        return render(request, 'store/checkout_success.html')

    # show the "Confirm order" page
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)
