from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.explore_view, name='explore'),
    path('community/<int:community_id>/', views.community_detail_view, name='community_detail'),
    path('community/<int:community_id>/join/', views.join_community_view, name='join_community'),
    path('community/<int:community_id>/leave/', views.leave_community_view, name='leave_community'),
    path('matches/', views.music_matches_view, name='music_matches'),
    path('matches/calculate/<int:user_id>/', views.calculate_match_view, name='calculate_match'),
]

