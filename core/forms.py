from django import forms
from django.forms import ModelForm
from .models import Match, Team


class MatchFormAdmin(ModelForm):
    class Meta:
        model = Match
        fields = ('gametype', 'datetime', 'creator',)
        labels = {
            'gametype': 'gametype',
            'datetime': 'YYYY-MM-DD HH:MM:SS',
            'creator': 'creator',

        }
        widgets = {
            'gametype': forms.Select(attrs={'class':'form-control', 'placeholder':'Gametype'}),
            'creator': forms.Select(attrs={'class':'form-select', 'placeholder':'Creator'}),
            'datetime': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Date / Time'}),
        }

# User Event Form
class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ('gametype',)
        labels = {
            'gametype': 'gametype',


        }
        widgets = {
            'gametype': forms.Select(attrs={'class':'form-control', 'placeholder':'Gametype'}),
        }




# User Team Form
class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('gametype', 'teamname','teammembers',)
        labels = {
            'gametype': 'Gametype',
            'teamname': '',
            'teammembers':'Team Members',

        }
        widgets = {
            'gametype': forms.Select(attrs={'class':'form-control', 'placeholder':'Gametype'}),
            'teamname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team Name'}),
            'teammembers': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Team Members'}),
        }

class TeamFormAdmin(ModelForm):
    class Meta:
        model = Team
        fields = ('gametype', 'teamname', 'captain', 'teammembers',)
        labels = {
            'gametype': 'Gametype',
            'teamname': '',
            'captain': 'Captain',
            'teammembers':'Team Members',
        }
        widgets = {
            'gametype': forms.Select(attrs={'class':'form-control', 'placeholder':'Gametype'}),
            'teamname': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Team Name'}),
            'captain': forms.Select(attrs={'class':'form-control', 'placeholder':'Captain'}),
            'teammembers': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Team Members'}),
        }
