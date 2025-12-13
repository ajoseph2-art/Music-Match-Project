from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='user_profile'),
    path('server_info/', views.server_info, name='server_info'),
    # Playlist URLs
    path('playlists/', views.my_playlists_view, name='my_playlists'),
    path('playlists/create/', views.create_playlist_view, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail_view, name='playlist_detail'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist_view, name='delete_playlist'),
]

