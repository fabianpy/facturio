from django.urls.conf import path

from apps.principal import views, forms
from django.contrib.auth import views as auth_views

app_name = 'principal'
urlpatterns = [
    path('index/', views.MainView.as_view(), name='index'),
    path('login', auth_views.login, {'authentication_form': forms.PrincipalAuthenticationForm}, name='login'),
    path('logout', auth_views.logout, name='logout'),
]
