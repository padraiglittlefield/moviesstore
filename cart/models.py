from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class CheckoutFeedback(models.Model):
    name = models.CharField(max_length=100, blank=True)  # optional
    statement = models.TextField()
    date = models.DateTimeField(auto_now_add=True)  # for ordering
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional user link
    
    def __str__(self):
        return f"{self.name or 'Anonymous'}: {self.statement[:30]}"