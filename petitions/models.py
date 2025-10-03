from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.movie_title}"
    
    def yes_votes_count(self):
        return self.vote_set.filter(vote_type='yes').count()
    
    def no_votes_count(self):
        return self.vote_set.filter(vote_type='no').count()

class Vote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('petition', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.vote_type} on {self.petition.movie_title}"
