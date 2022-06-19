"""memes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import settings
from backend.views import *

router = ExtendedDefaultRouter()
router.register(r'memes', MemeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/like/<int:id>', like, name='like'),
    path('api/feed/', feed, name='feed'),
    path('api/feed_new/', feed_new, name='feed_new'),
    path('api/top/', top, name='top'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
