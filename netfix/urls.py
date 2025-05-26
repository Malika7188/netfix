from django.urls import re_path as url
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('services/', include('services.urls')),
    path('register/', include('users.urls')),
    path('login/', include('users.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('customer/<slug:name>/', v.customer_profile, name='customer_profile'),
    path('company/<slug:name>/', v.company_profile, name='company_profile')
]