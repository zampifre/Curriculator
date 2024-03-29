import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from yamlfield.fields import YAMLField
from django.dispatch import receiver

class Profile(models.Model):
    """
    Profilo utente, associato ad uno user (one to one field con django User), con i relativi dati anagrafici.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascita = models.DateField(null=True)
    luogo_nascita = models.CharField(max_length=50, null=True, blank=True)
    sesso = models.CharField(max_length=1, choices=(('M', 'Maschio'), ('F', 'Femmina')), null=True)
    telefono = models.CharField(max_length=20, null=True, blank=False)
    foto = models.ImageField(null=True, blank=True, upload_to='images', default='static/images/unknow.png')

    class Meta:
        verbose_name_plural = "Profili"

    def __str__(self):
        return f'{self.user.username}, {self.user.first_name}, {self.user.last_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Genera un'istanza di Profile automaticamente con la creazione di uno user.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salva i dati dello User all'intero dell'istanza Profile generata.
    """
    instance.profile.save()


class Curriculum(models.Model):
    """
    Oggetto Curriculum, associato ad un Profile, contenente la data di creazione e di modifica.
    """
    profilo = models.ForeignKey(Profile, on_delete=models.CASCADE)
    data_creazione = models.DateField(default=datetime.date.today)
    data_modifica = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name_plural = "Curriculum"

    def __str__(self):
        return f'{self.profilo}, {self.data_creazione}, {self.data_modifica}'

class Sezione(models.Model):
    """
    Sezione associata ad un'istanza di Curriculum. Ogni Curriculum conterrà più sezioni, costituite da un titolo
    e un booleano per l'attivazione dell'ordinamento manuale da parte dell'utente.
    """
    titolo = models.CharField(max_length=100, null=False)
    curriculum = models.ForeignKey(Curriculum, default=None, on_delete=models.CASCADE)
    ordinamento_manuale = models.BooleanField(default=False, blank=True, null=False)

    def delete_url(self):
        """
        Metodo per l'eliminazione di un'istanza Sezione.
        """
        return reverse('delete-sezione', kwargs={'pk': self.id})

    class Meta:
        verbose_name_plural = "Sezioni"

    def __str__(self):
        return self.titolo

class Elemento(models.Model):
    """
    Elemento relativo ad una Sezione. Ogni Sezione conterrà diversi Elementi associati ad essa.
    Contiene un titolo, date di inizio e fine, campi (coppie chiave-valore in formato YAML), la relativa sezione e
    una posizione assegnata per l'ordinamento interno alla Sezione.
    """
    titolo = models.CharField(max_length=200, null=False)
    data_inizio = models.DateField(null=True, default=None, blank=True)
    data_fine = models.DateField(null=True, default=None, blank=True)
    campi = YAMLField()
    sezione = models.ForeignKey(Sezione, default=None, on_delete=models.CASCADE)
    posizione = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Elementi"
        ordering = ['posizione']

    def __str__(self):
        return self.titolo
