from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.get_csrf, name='get_csrf'),
    path('let_manipulate_our_api_from_here', views.let_manipulate_our_api_from_here, name='api'),
]


