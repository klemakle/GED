from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Eleve, Document, Commentaire, Question, Reponse


class FormulaireCreationUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password1', 'password2']


class EleveForm(ModelForm):
    class Meta:
        model = Eleve
        fields ='__all__'
        exclude = ['user']


"""
class Creationdoc(ModelForm):
    class Meta:
        model = Document
        fields = ['titre','fichier','text','classe_doc', 'genie_doc']
        
"""



class CommentForm(forms.ModelForm):
    contenu = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control z-depth-1', 'placeholder':'votre commentaire !!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Commentaire
        fields = ('contenu',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question',)


    
class ReponseForm(forms.ModelForm):
    reponse = forms.CharField(label="", widget =forms.Textarea(attrs={'class':'form-control', 'placeholder':'votre réponse...', 'rows':'3', 'cols':'5'}))
    class Meta:
        model = Reponse
        fields = ('reponse',)

