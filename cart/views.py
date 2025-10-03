from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item, CheckoutFeedback
from django.contrib.auth.decorators import login_required
from .forms import CheckoutFeedbackForm

@login_required
def purchase(request):
    print("Purchase view called") # Debug print
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    
    if (movie_ids == []):
        return redirect('cart.index')
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    
    request.session['cart'] = {}
    
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    template_data['show_feedback_popup'] = True
    
    print("Template data:", template_data) # Debug print
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
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    
    return render(request, 'cart/index.html', {'template_data': template_data})

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

def checkout_feedback(request):
    if request.method == "POST":
        form = CheckoutFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            
            # Return JSON response for AJAX popup requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your feedback!'
                })
            else:
                return redirect('feedback_list')
        else:
            # Return JSON response with errors for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
    else:
        form = CheckoutFeedbackForm()
    
    return render(request, "cart/checkout_feedback.html", {"form": form})

def feedback_list(request):
    feedbacks = CheckoutFeedback.objects.order_by('-date')
    return render(request, "cart/feedback_list.html", {"feedbacks": feedbacks})