from django.shortcuts import render, redirect

from .models import *
from .forms import RegistrationForm, TournamentForm


# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def table(request):
    members = Member.objects.all()
    
    context = {
        "members":members
    }

    return render(request, 'main/table.html', context)
    

def tournament(request):
    tournaments = Tournament.objects.all()

    context = {
        'tournaments': tournaments
    }

    return render(request, 'main/tournament.html', context)


def create_member(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return redirect('table')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})



def generate_tournament(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TournamentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return redirect('table')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TournamentForm()

    return render(request, 'main/generate_tournament.html', {'form': form})

def generate_matches(request):
    if request.method == 'POST':
        tournament_id = request.POST.get('tournament_id')
        tournament_members = Tournament.objects.get(id=tournament_id).generate_members()
        matches = Match.generate_matches(Match, tournament_id=tournament_id)

        context = {
            'matches': matches,
            'tournament_members': tournament_members,
        }

        return render(request, 'main/tournament.html', context)

    tournaments = Tournament.objects.all()

    context = {
        'tournaments': tournaments
    }
    
    return render(request, 'main/generator.html', context)


