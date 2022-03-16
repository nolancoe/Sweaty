from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView
from .models import Match, Team
from core.forms import MatchFormAdmin, MatchForm, TeamFormAdmin, TeamForm
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'core/home.html', {})

class MatchView(ListView):
    model = Match
    template_name = 'core/matches.html'

class MatchDetailView(DetailView):
    model = Match
    template_name = 'core/match_details.html'

def create_match(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = MatchFormAdmin(request.POST)
            if form.is_valid():
                    form.save()
                    return  HttpResponseRedirect('/create_match?submitted=True')
        else:
            form = MatchForm(request.POST)
            if form.is_valid():
                #form.save()
                match = form.save(commit=False)
                match.creator = request.user # logged in user
                match.save()
                return  HttpResponseRedirect('/matches')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = MatchFormAdmin
        else:
            form = MatchForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'core/create_match.html', {'form':form, 'submitted':submitted})

def create_team(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = TeamFormAdmin(request.POST)
            if form.is_valid():
                    form.save()
                    return  HttpResponseRedirect('/create_team?submitted=True')
        else:
            form = TeamForm(request.POST)
            if form.is_valid():
                #form.save()
                team = form.save(commit=False)
                team.captain = request.user # logged in user
                team.save()
                return  HttpResponseRedirect('/matches')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = TeamFormAdmin
        else:
            form = TeamForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'core/create_team.html', {'form':form, 'submitted':submitted})


class TeamView(ListView):
    model = Team
    template_name = 'core/teams.html'

class TeamDetailView(DetailView):
    model =  Team
    template_name = 'team_details.html'
