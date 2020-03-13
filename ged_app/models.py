from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from django.core.files import file


#Poser des questions
# Create your models here.


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







class Question(models.Model):
    eleve_id= models.ForeignKey(Eleve,  on_delete=models.CASCADE) 
    aime = models.IntegerField(default=0)
    question = models.TextField(max_length=200, null=False)
    date_question = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "'{}... ?'  posé par  {}".format(self.question[:20], str(self.eleve_id.name))

    




class Reponse(models.Model):
    el = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    date_reponse = models.DateTimeField( auto_now_add=True)
    reponse = models.TextField(max_length=500, null = True)

    def __str__(self):
        return '{} --- repondu par {}'.format(self.reponse[:20], str(self.el.name))
