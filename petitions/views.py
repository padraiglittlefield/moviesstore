from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition, Vote
from django.contrib import messages

def index(request):
    petitions = Petition.objects.all().order_by('-created_at')
    
    # Add vote information for the current user
    petition_list = []
    for petition in petitions:
        petition_data = {
            'petition': petition,
            'user_voted': False,
            'user_vote': None
        }
        
        if request.user.is_authenticated:
            try:
                vote = Vote.objects.get(petition=petition, user=request.user)
                petition_data['user_voted'] = True
                petition_data['user_vote'] = vote.vote_type
            except Vote.DoesNotExist:
                pass
        
        petition_list.append(petition_data)
    
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petition_list'] = petition_list
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Create Petition'
        return render(request, 'petitions/create.html', {'template_data': template_data})
    elif request.method == 'POST':
        movie_title = request.POST.get('movie_title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not movie_title or not description:
            template_data = {}
            template_data['title'] = 'Create Petition'
            template_data['error'] = 'Both movie title and description are required.'
            template_data['movie_title'] = movie_title
            template_data['description'] = description
            return render(request, 'petitions/create.html', {'template_data': template_data})
        
        petition = Petition()
        petition.movie_title = movie_title
        petition.description = description
        petition.created_by = request.user
        petition.save()
        
        messages.success(request, 'Petition created successfully!')
        return redirect('petitions.index')

@login_required
def vote(request, id):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=id)
        vote_type = request.POST.get('vote_type')
        
        if vote_type not in ['yes', 'no']:
            messages.error(request, 'Invalid vote type.')
            return redirect('petitions.index')
        
        # Check if user has already voted
        existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, 'Your vote has been updated!')
        else:
            # Create new vote
            vote_obj = Vote()
            vote_obj.petition = petition
            vote_obj.user = request.user
            vote_obj.vote_type = vote_type
            vote_obj.save()
            messages.success(request, 'Your vote has been recorded!')
        
        return redirect('petitions.index')
    else:
        return redirect('petitions.index')

def show(request, id):
    petition = get_object_or_404(Petition, id=id)
    
    # Check if user has voted
    user_voted = False
    user_vote = None
    if request.user.is_authenticated:
        try:
            vote = Vote.objects.get(petition=petition, user=request.user)
            user_voted = True
            user_vote = vote.vote_type
        except Vote.DoesNotExist:
            pass
    
    template_data = {}
    template_data['title'] = petition.movie_title
    template_data['petition'] = petition
    template_data['user_voted'] = user_voted
    template_data['user_vote'] = user_vote
    return render(request, 'petitions/show.html', {'template_data': template_data})
