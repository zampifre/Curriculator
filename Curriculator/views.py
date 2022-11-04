from django.views.generic import TemplateView, CreateView
from CurriculatorApp.models import Profile
class Homepage(TemplateView):
    template_name = 'Curriculator/home.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(Homepage, self).get_context_data(**kwargs)
            profilo = Profile.objects.get(user=self.request.user)
            context['utente'] = profilo
            return context
