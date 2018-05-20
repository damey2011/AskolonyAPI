"""AskolonyAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from rest_framework_swagger.views import get_swagger_view

from AskolonyAPI import settings

schema_view = get_swagger_view("Askolony API Documentation")

admin.site.site_header = 'Askolony Admin'

urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^api/accounts/', include('Account.urls')),
    url(r'^api/posts/', include('Post.urls')),
    url(r'^api/questions/', include('Questions.urls')),
    url(r'^api/topics/', include('Topic.urls')),
    url(r'^api/polls/', include('Poll.urls')),
    url(r'^api/messages/', include('Messages.urls')),
    url(r'^api/notifications/', include('Notification.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
