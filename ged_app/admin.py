from django.contrib import admin
from django.apps import apps
# Register your models here.
from .models import Eleve, Document, Commentaire, Question, Reponse

mode = apps.get_models()

"""
for i in mode:
    try:
        admin.site.register(i)

    except admin.sites.AlreadyRegistered:
        pass
"""    

admin.site.register(Eleve)
admin.site.register(Document)
admin.site.register(Commentaire)
admin.site.register(Question)
admin.site.register(Reponse)
