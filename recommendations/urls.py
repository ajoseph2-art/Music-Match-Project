from django.urls import path
from . import views

urlpatterns = [
    path('', views.spotify_recommendations_view, name='recommendations'),
    path('spotify/', views.spotify_recommendations_view, name='spotify_recommendations'),
    path('spotify/search/', views.search_spotify_view, name='spotify_search'),
    path('spotify/similar/', views.spotify_similar_view, name='spotify_similar'),
]

