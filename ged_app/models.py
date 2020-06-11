from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.

# Modele d'eleves comportant:
#     1- un nom en chaine de caracteres
#     2- un Age en Entier
#     3- un genre (homme ou femme)
#     4- la classe de l'élève en entier
#     5- Son domaine (génie) en entier
#     6- la photo de Profile de l'élève
class Eleve(models.Model):
    LISTE_CLASSE = (
        ('TC1', 'TC1'),
        ('TC2','TC2'),
        ('DIC1','DIC1'),
        ('DIC2','DIC2'),
        ('DIC3','DIC3')
    )

    LISTE_GENIE = (
        ('GIT','Génie Informatique et Télécommunications'),
        ('Génie Civil','Génie Civil'),
        ('Génie Electromécanique','Génie Electro-Mécanique'),
        ('Tronc Commun', 'Tronc Commun')
    )
    user = models.OneToOneField(User,null = True, blank=True,on_delete=models.CASCADE)
    name = models.CharField( max_length=150, null=True)
    age = models.IntegerField(null=True)
    sexe = models.CharField(max_length=80, choices = [('Homme', 'Homme' ), ('Femme', 'Femme')], null=True)
    classe = models.CharField(max_length=50 , null =True ,  choices = LISTE_CLASSE)
    genie = models.CharField(max_length=100, null = True, choices = LISTE_GENIE)
    photo_profile = models.ImageField(default ="user-default.png",null = True, blank = True )
    
    
    def __str__(self):
        if self.name != None:
            return self.name
        else:
            return "%% No name %%"

#=============================================================================================================================================
            
    

# Modele du document à publier comportant:
#     1- l'auteur du document qui est un élève
#     2- le titre du document en chaines de caracères
#     3- le document lui-même qui est un fichier
#     4- le niveau auquel le document faire reference: la classe
#     5- le domaine auquel le document fait reference: le genie
#     6- la date de publication du document
class Document(models.Model):
    LISTE_GENIE = (
        ('GIT','Génie Informatique et Télécommunications'),
        ('Génie Civil','Génie Civil'),
        ('Génie Electromécanique','Génie Electro-Mécanique'),
        ('Tronc Commun', 'Tronc Commun')
    )
    LISTE_CLASSE = (
        ('TC1', 'TC1'),
        ('TC2','TC2'),
        ('DIC1','DIC1'),
        ('DIC2','DIC2'),
        ('DIC3','DIC3')
    )
    author = models.ForeignKey(Eleve, on_delete=models.CASCADE, null = True)
    titre = models.CharField(max_length=100, null = True)
    fichier = models.FileField(upload_to='media/', null= True, blank=True)
    text = models.TextField(max_length=1000, null=True, blank=True)
    classe_doc = models.CharField(max_length=50 , null =True ,  choices = LISTE_CLASSE)
    genie_doc = models.CharField(max_length=100, null = True, choices = LISTE_GENIE)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    
    def __str__(self):
        if self.titre != None:
            return self.titre
        else : 
            return " no title"

#=============================================================================================================================================




# Modèle de Commentaire comportant:   
#     1- l'auteur du commentaire qui est un élève
#     2- le document commenté qui est un Document
#     3- la réponse à un commentaire qui est aussi un commentaire
#     4- le nombre de votes positifs au commentaire dénommé "CHOC" ( à mettre en place)
#     5- le nombre de votes négatifs à un commentaire qui entrainera la supression du commentaire
#     6- le contenu du commentaire lui-même qui est un texte
class Commentaire(models.Model):
    author_id = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    doc = models.ForeignKey(Document, on_delete=models.CASCADE)
    reply = models.ForeignKey('Commentaire', null=True, related_name='repliques', on_delete = models.CASCADE)
    date_commentaire = models.DateTimeField(auto_now_add=True, null=True)
    choc = models.IntegerField(default=0)
    signaler = models.IntegerField(default=0)
    contenu = models.TextField(max_length=1000, null = True)

    def __str__(self):
        return '{} ---- COMMENT BY {}'.format(self.doc.titre, str(self.author_id.name))

#=============================================================================================================================================




# Modele de question. Les questions permettent aux utilisateurs de poser n'importe quoi sur le site et d'attendre des réponses venant des autres utilisateurs
#     1- l'auteur de la question qui est un élève
#     2- le nombre votes positifs à la question dénommmé ici "aime"
#     3- le contenu de la question elle-même
#     4- la date de publication de la question
class Question(models.Model):
    eleve_id= models.ForeignKey(Eleve,  on_delete=models.CASCADE) 
    aime = models.IntegerField(default=0)
    question = models.TextField(max_length=200, null=False)
    date_question = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "'{}... ?'  posé par  {}".format(self.question[:20], str(self.eleve_id.name))

#=============================================================================================================================================




# Modèle de reponse comportant:
#     1- l'auteur de la réponse qui est un élève
#     2- la question répondue
#     3- le nombre de votes positives à la réponse
#     4- la date de réponse
#     5- la réponse elle-même qui est un texte
class Reponse(models.Model):
    el = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    date_reponse = models.DateTimeField( auto_now_add=True)
    reponse = models.TextField(max_length=500, null = True)

    def __str__(self):
        return '{} --- repondu par {}'.format(self.reponse[:20], str(self.el.name))
