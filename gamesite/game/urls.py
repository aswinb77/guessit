from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/me/', views.api_me),
    path('api/name/', views.api_set_name),
    path('api/new/', views.api_new),
    path('api/guess/<int:game_id>/', views.api_guess),
    path('api/leaderboard/', views.api_leaderboard),
]