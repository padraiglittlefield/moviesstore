from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition, Vote

def index(request):
    petitions = Petition.objects.all().order_by("-created_at")
    template_data = {'title': 'Petitions', 'petitions':petitions}
    return render(request, 'petitions/index.html', {"template_data":template_data})

@login_required
def create(request):
    if request.method == "POST":
        Petition.objects.create(
            movie_title = request.POST['movie_title'],
            description = request.POST['description'],
            created_by = request.user
        )
    template_data = {"title":'Create Petition'}
    return render(request, 'petitions/create.html', {"template_data":template_data})

@login_required
def vote(request, id):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=id)
        Vote.objects.update_or_create(
            petition = petition,
            user=request.user,
            defaults={'vote_type':'yes'}
        )
    return redirect('petitions.index')
