from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, TemplateView
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            u_name = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=u_name, first_name=first_name, last_name=last_name, password=pwd)
            login(request, user)
            messages.success(request, 'Account creato correttamente')
            return redirect('homepage')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/registration.html', {'user_form': form})

class Profilo(DetailView):
    template_name = 'profile/profilo_view.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(Profilo, self).get_context_data(**kwargs)
        context['curriculum'] = Curriculum.objects.all()
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfiloForm
    template_name = 'profile/aggiorna-profilo.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user.profile)
        profile_form = ProfiloForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Il tuo profilo è stato aggiornato correttamente!')
            return redirect(reverse('CurriculatorApp:profilo', kwargs={'pk': self.request.user.pk}))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
