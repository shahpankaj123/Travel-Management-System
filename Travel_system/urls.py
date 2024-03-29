"""
URL configuration for Travel_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from .views import Contact,About,Services


urlpatterns = [
    path('admin/', admin.site.urls, name='adminpannel'),
    path("", include("bus_reserve.urls"), name="main"),
    path('user/',include('account.urls')),
    path('contact/',Contact,name='contact'),
    path('about/',About,name='about'),
    path('services/',Services,name='services'),
    #path("test/", test, name="lollll")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)