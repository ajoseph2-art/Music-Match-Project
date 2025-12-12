from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendations_view, name='recommendations'),
    path('discovery/', views.discovery_swipe_view, name='discovery_swipe'),
    path('swipe/<int:song_id>/<str:action>/', views.swipe_action_view, name='swipe_action'),
]

