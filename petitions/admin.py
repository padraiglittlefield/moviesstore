from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_title', 'created_by', 'created_at', 'yes_votes_count', 'no_votes_count')
    list_filer = ('created_at',)
    search_fields = ('movie_title', 'description')
    readonly_fields = ('created_at',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'petition', 'user', 'vote_type' ,'voted_at')
    list_filer = ('vote_type', 'voted_at')
    search_fields = ('movie_title', 'description')
    readonly_fields = ('voted_at',)
    