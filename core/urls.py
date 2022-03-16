from django.urls import path
from .views import MatchView, MatchDetailView, create_match, create_team, TeamView, TeamDetailView
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('matches/', MatchView.as_view(), name="matches"),
    path('match/<int:pk>', MatchDetailView.as_view(), name='match-detail'),
    path('create_match/', views.create_match, name='create_match'),
    path('create_team/', views.create_team, name='create_team'),
    path('teams/', TeamView.as_view(), name="teams"),
    path('team/<int:pk>', TeamDetailView.as_view(), name='team-detail'),
]
