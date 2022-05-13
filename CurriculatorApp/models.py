import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_yaml_field.fields import YAMLField
from django.dispatch import receiver

#Dentro a User di django ci sono già nome utente, nome, cognome e e-mail
class Profile(models.Model):
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
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#Ho impostato entrambe le date senza obbligo di inserimento in modo tale che:
#   - solo data inizio --> evento in corso
#   - solo fine --> evento concluso
#   - inizio e fine --> evento concluso
class Elemento(models.Model):
    titolo = models.CharField(max_length=200, null=False)
    data_inizio = models.DateField(null=True, default=None)
    data_fine = models.DateField(null=True, default=None)
    campi = YAMLField()

    class Meta:
        verbose_name_plural = "Elementi"

    def __str__(self):
        return self.titolo

class Sezione(models.Model):
    titolo = models.CharField(max_length=100, null=False)
    elementi = models.ManyToManyField(Elemento, default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sezioni"

    def __str__(self):
        return self.titolo

class Curriculum(models.Model):
    profilo = models.ForeignKey(Profile, on_delete=models.CASCADE)
    data_creazione = models.DateField(default=datetime.date.today)
    data_modifica = models.DateField(default=datetime.date.today)
    sezione = models.ManyToManyField(Sezione, default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Curriculum"

    def __str__(self):
        return f'{self.profilo}, {self.data_creazione}, {self.data_modifica}'
