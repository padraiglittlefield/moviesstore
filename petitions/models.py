from django.db import models
from django.contrib.auth.models import User


class Petition(models.Model):
    movie_title = models.CharField(max_length=255) 
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.movie_title

    def yes_votes(self):
        return self.vote_set.filter(vote_type='yes').count()

class Vote(models.Model):

    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])

    class Meta:
        unique_together = ('petition', 'user')