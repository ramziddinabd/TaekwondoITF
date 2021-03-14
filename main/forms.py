from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name','birth_date','gender','weight','level','team']

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament

        fields = ['gender','min_birth_date','max_birth_date','min_weight','max_weight','level','match_type']
