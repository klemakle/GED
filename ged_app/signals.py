from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Eleve


def eleve_profile(sender, instance, created, **kwars):
    if created:
        group1 = Group.objects.get(name='Eleve')
         #group2 = Group.objects.get(name = '')     
        instance.groups.add(group1)

        Eleve.objects.create(
            user=instance,
            name = instance.first_name, # username à changer par first_name
            )
        print('élève ajouté !!')


post_save.connect(eleve_profile, sender=User)



