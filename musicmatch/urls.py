"""
URL configuration for musicmatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from playlists import views as playlists_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("playlists.urls")),
    path("accounts/", include("accounts.urls")),
    path("communities/", include("communities.urls")),
    path("recommendations/", include("recommendations.urls")),
    path("server_info/", playlists_views.server_info, name="server_info"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
