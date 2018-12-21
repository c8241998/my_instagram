"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from final.settings import MEDIA_ROOT
from ins import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),

    url(r'^me$', views.me, name='me'),
    url(r'^me/changeEmail$', views.change_email, name='changeEmail'),
    url(r'^me/changeUsername$', views.change_username, name='changeUsername'),
    url(r'^me/changePassword$', views.change_password, name='changePassword'),
    url(r'^me/changeProfile$', views.change_profile, name='changeProfile'),

    url(r'^square$', views.square, name='square'),
    url(r'^like$', views.like, name='like'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^uploadphoto$', views.upload_photo, name='uploadphoto'),
    url(r'^post$', views.post, name='post'),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    url(r'^', views.home, name='home'),
]
