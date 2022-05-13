from django.urls import path
from CurriculatorApp import views
from CurriculatorApp.views import *

app_name = "CurriculatorApp"
urlpatterns = [
    path('user-register/', views.register, name='user-register'),
    path('<int:pk>/profile/', Profilo.as_view(), name='profilo'),
    path('update-profile/', ProfileUpdateView.as_view(), name='aggiorna-profilo'),
]
