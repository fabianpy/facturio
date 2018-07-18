from django.urls.conf import path

from apps.principal import views

app_name = 'principal'
urlpatterns = [
    path('index/', views.MainView.as_view(), name='index'),
]