"""GameStop URL Configuration

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


from django.contrib import admin
from django.urls import path,include
from Product.views import home_view
from Product.views import contact_page
from Product.views import about_page
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('product/',include('Product.urls',namespace='product')),
    path('',home_view,name='home'),
    path('contact/',contact_page,name='contact'),
    path('product/', include('django.contrib.auth.urls')),
    path('admin/',admin.site.urls),
    path('about/',about_page,name='about'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
