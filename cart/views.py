from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from .forms import CheckoutFeedbackForm

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())

    if movie_ids == []:
        return redirect('cart.index')
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order.objects.create(user=request.user, total=cart_total)

    for movie in movies_in_cart:
        Item.objects.create(
            movie=movie,
            price=movie.price,
            order=order,
            quantity=cart[str(movie.id)]
        )

    request.session['cart'] = {}

    # Handle feedback submission
    if request.method == "POST":
        form = CheckoutFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.order = order
            feedback.save()
            return redirect('cart.index')  # back to cart/home after feedback
    else:
        form = CheckoutFeedbackForm()

    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
        'form': form,
    }
    return render(request, 'cart/purchase.html', {'template_data': template_data})


def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart =Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart,movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',{'template_data': template_data})

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')