from django.views.generic import TemplateView, CreateView

class Homepage(TemplateView):
    template_name = 'Curriculator/home.html'
