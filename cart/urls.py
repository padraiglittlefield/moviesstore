from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('checkout-feedback/', views.checkout_feedback, name='checkout_feedback'),
    path('feedback-list/', views.feedback_list, name='feedback_list'),

]