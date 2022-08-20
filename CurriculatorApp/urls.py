from django.urls import path
from CurriculatorApp import views
from CurriculatorApp.views import *

app_name = "CurriculatorApp"
urlpatterns = [
    path('user-register/', views.register, name='user-register'),
    path('<int:pk>/profile/', Profilo.as_view(), name='profilo'),
    path('update-profile/', ProfileUpdateView.as_view(), name='aggiorna-profilo'),
    path('create-curriculum/', views.CurriclumCreate.as_view(), name='crea-curriculum'),
    path('<int:pk>/delete-curriculum/', CurriculumDelete.as_view(), name='cancella-curriculum'),
    path('<int:pk>/detail-curriculum/', CurriculumDetail.as_view(), name='dettagli-curriculum'),
    path('delete/<int:pk>', views.delete_sezione, name='delete-sezione'),

]
