from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [path('jaka_pogoda/', views.jaka_pogoda, name="jaka_pogoda"),]