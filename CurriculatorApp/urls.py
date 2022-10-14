from django.urls import path
from CurriculatorApp import views
from CurriculatorApp.views import *

app_name = "CurriculatorApp"
urlpatterns = [
    path('user-register/', views.register, name='user-register'),
    path('<int:pk>/profile/', Profilo.as_view(), name='profilo'),
    path('update-profile/', ProfileUpdateView.as_view(), name='aggiorna-profilo'),
    path('create-curriculum/', views.CurriclumCreate.as_view(), name='crea-curriculum'),
    path('delete-curriculum/<int:pk>', views.curriculum_delete, name='delete-curriculum'),
    path('<int:pk>/detail-curriculum/', CurriculumDetail.as_view(), name='dettagli-curriculum'),
    path('delete-sezione/<int:pk>', views.delete_sezione, name='delete-sezione'),
    path('delete-elemento/<int:pk>', views.delete_elemento, name='delete-elemento'),
    path('crea-elemento/', views.elemento_create, name='newelement'),
    path('crea-sezione/', views.sezione_create, name='newsection'),
    path('aggiorna-elemento/', views.element_update, name='editelement'),
    path('aggiorna-sezione/', views.sezione_update, name='editsection'),
    path('ordinamento-elemento/', views.sort, name='sortelement'),
    path('ordinamento-default/', views.sort_manual, name='sortdefault'),
    path('setting-manuale/', views.set_manual, name='setmanual'),
    path('create-cv/', views.new_cv, name='create_cv'),
    path('<int:pk>/pdf-template/', CVTemplatePdf.as_view(), name='templatepdf'),
]
