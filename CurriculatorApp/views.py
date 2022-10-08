import re
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from .forms import *
from django.contrib import messages
from django.views.generic.edit import CreateView
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
        context['curriculum'] = Curriculum.objects.filter(profilo=kwargs['object'].id)
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    profile_form = ProfiloForm
    template_name = 'profile/aggiorna-profilo.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        profile_form = ProfiloForm(post_data, file_data, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Il tuo profilo è stato aggiornato correttamente!')
            return redirect(reverse('CurriculatorApp:profilo', kwargs={'pk': self.request.user.pk}))

        context = self.get_context_data(profile_form=profile_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CurriclumCreate(CreateView):
    model = Curriculum
    fields = []
    template_name = 'profile/create-curriculum.html'

    def get_initial(self):
        initial = super(CurriclumCreate, self).get_initial()
        initial = initial.copy()
        profile = get_object_or_404(Profile, user=self.request.user)
        date_creation = datetime.date.today()
        date_modifica = datetime.date.today()
        initial['profilo'] = profile
        initial['data_creazione'] = date_creation
        initial['data_modifica'] = date_modifica
        return initial

    def form_valid(self, form):
        form.instance.profilo = self.request.user.profile
        return super(CurriclumCreate, self).form_valid(form)

    def get_success_url(self):
        profile_id = self.request.user.pk
        return reverse_lazy('CurriculatorApp:profilo', kwargs={'pk': profile_id})

def curriculum_delete(request, pk):
    curriculum = Curriculum.objects.get(id=pk)
    curriculum.delete()
    messages.error(request, 'Sezione eliminata con successo!')
    return redirect(request.META['HTTP_REFERER'])

class CurriculumDetail(DetailView):
    model = Curriculum
    template_name = 'profile/curriculum-detail.html'

    def get_context_data(self, **kwargs):
        context = super(CurriculumDetail, self).get_context_data(**kwargs)
        context['form_elemento'] = ElementForm()
        context['form_sezione'] = SectionForm()
        context['curriculum'] = kwargs['object']
        context['sezioni'] = Sezione.objects.filter(curriculum=kwargs['object'].id)
        print(kwargs['object'].profilo)
        context['elementi'] = Elemento.objects.filter(sezione__in=context['sezioni'])
        return context


def delete_elemento(request, pk):
    elemento = Elemento.objects.get(id=pk)
    cv = Curriculum.objects.get(id=elemento.sezione.curriculum.id)
    cv.data_modifica = datetime.date.today()
    cv.save()
    elemento.delete()
    messages.error(request, 'Elemento eliminato con successo!')
    return redirect(request.META['HTTP_REFERER'])

def delete_sezione(request, pk):
    sezione = Sezione.objects.get(id=pk)
    cv = Curriculum.objects.get(id=sezione.curriculum.id)
    cv.data_modifica = datetime.date.today()
    cv.save()
    sezione.delete()
    messages.error(request, 'Sezione eliminata con successo!')
    #refresh della pagina corrente
    return redirect(request.META['HTTP_REFERER'])
    #return redirect('CurriculatorApp:dettagli-curriculum', kwargs={'pk': sezione.curriculum.pk})

def elemento_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        elemento_titolo = request.POST['titolo']
        elemento_data_inizio = request.POST['data_inizio']
        if elemento_data_inizio == '':
            elemento_data_inizio = None
        elemento_data_fine = request.POST['data_fine']
        if elemento_data_fine == '':
            elemento_data_fine = None
        elemento_sezione = Sezione.objects.get(id=request.POST['sezione'])
        elemento_campi = request.POST['campi']
        if elemento_titolo and elemento_campi and elemento_sezione:
            print(elemento_data_inizio)
            print(elemento_data_fine)
            elemento = Elemento.objects.create(titolo=elemento_titolo, data_inizio=elemento_data_inizio,
                                               data_fine=elemento_data_fine, sezione=elemento_sezione,
                                               campi=elemento_campi)
            cv = elemento_sezione.curriculum
            cv.data_modifica = datetime.date.today()
            cv.save()
            elemento.save()
            return redirect(request.META['HTTP_REFERER'])

def element_update(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        elemento = Elemento.objects.get(id=request.POST['id_elemento'])
        elemento.titolo = request.POST['titolo']
        elemento.data_inizio = request.POST['data_inizio']
        if elemento.data_inizio == '':
            elemento.data_inizio = None
        elemento.data_fine = request.POST['data_fine']
        if elemento.data_fine == '':
            elemento.data_fine = None
        elemento.campi = request.POST['campi']
        elemento.sezione = Sezione.objects.get(id=request.POST['sezione'])
        if elemento.titolo and elemento.campi and elemento.sezione:
            cv = elemento.sezione.curriculum
            cv.data_modifica = datetime.date.today()
            cv.save()
            elemento.save()
            return redirect(request.META['HTTP_REFERER'])

def sezione_create(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        sezione_titolo = request.POST['titolo']
        sezione_curriculum = Curriculum.objects.get(pk=request.POST['curriculum'])
        if sezione_titolo:
            sezione = Sezione.objects.create(titolo=sezione_titolo, curriculum=sezione_curriculum)
            sezione.save()
            sezione_curriculum.data_modifica = datetime.date.today()
            sezione_curriculum.save()
            return redirect(request.META['HTTP_REFERER'])

def sezione_update(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        print('entrato')
        sezione = Sezione.objects.get(id=request.POST['id_sezione'])
        sezione.titolo = request.POST['titolo']
        cv = Curriculum.objects.get(pk=sezione.curriculum.id)
        print(sezione)
        if sezione.titolo:
            sezione.save()
            cv.data_modifica = datetime.date.today()
            cv.save()
            return redirect(request.META['HTTP_REFERER'])

def sort(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        sezione = Sezione.objects.get(id=request.POST['sezione_id'])
        sezione.ordinamento_manuale = True
        sezione.save()
        list_id = [int(s) for s in re.findall(r'\b\d+\b', request.POST['ordine'])]
        lista_ordine = []
        for index, id_elemento in enumerate(list_id):
            elemento = Elemento.objects.get(pk=id_elemento)
            elemento.posizione = index
            elemento.save()
        return HttpResponse('ok')

def sort_manual(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        sezione = Sezione.objects.get(id=request.POST['id'])
        sezione.ordinamento_manuale = False
        sezione.save()
        elementi = Elemento.objects.filter(sezione__in=request.POST['id'])
        elementi_no_data_fine = elementi.filter(data_fine=None)
        elementi_no_data_fine = elementi_no_data_fine.order_by('-data_inizio')
        list_no_data_fine = elementi_no_data_fine.values_list('pk', flat=True)
        elementi_terminati = elementi.exclude(data_fine=None)
        elementi_terminati = elementi_terminati.order_by('-data_fine', '-data_inizio')
        list_terminati = elementi_terminati.values_list('pk', flat=True)
        queryset_finale = list(chain(list_no_data_fine, list_terminati))
        for index, id_elemento in enumerate(queryset_finale):
            elemento = Elemento.objects.get(pk=id_elemento)
            elemento.posizione = index
            elemento.save()
    return HttpResponse('ok')


def set_manual(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False

    if is_ajax:
        sezione = Sezione.objects.get(id=request.POST['id'])
        sezione.ordinamento_manuale = True
        sezione.save()
