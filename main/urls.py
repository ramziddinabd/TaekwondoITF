from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('table', views.table, name="table"),
    path('tournament', views.tournament, name="tournament"),
    path('create_member', views.create_member, name="create_member"),
    path('generate_tournament', views.generate_tournament, name="generate_tournament"),
    path('generate_matches', views.generate_matches, name="generate_matches"),
]