from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from ged_app.models import *

from django.contrib import messages

from django.contrib.auth.decorators import login_required


# Create your views here.
from .models import Eleve, Document, Commentaire, Question, Reponse
from .forms import *
from .permis import nonauthentifie_user, allowed_users, compte_autorise



#s'inscrire
@nonauthentifie_user
def inscrire(request):
    form = FormulaireCreationUser()
    if request.method == "POST" : 
        form = FormulaireCreationUser(request.POST)
        if form.is_valid():
            form.save() 
            name = form.cleaned_data.get('first_name')

            #group2 = Group.objects.get(name = '')                

            messages.success(request, 'Compte créé pour '+ name)
            return redirect('connecter')

    context = {'form' : form}
    return render(request, 'ged_app/inscrire.html', context)




#se connecter
@nonauthentifie_user
def connecter(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)
            return redirect('parametres')
        else: 
            messages.info(request, 'Pseudo ou Mot de passe incorrect')

    context = {}
    return render (request, 'ged_app/connexion.html', context)






#page de l'eleve
@login_required(login_url='connecter')
@allowed_users(allowed_roles=['Eleve'])
def page_eleve(request):
    d = Document.objects.all()
    qst = Question.objects.all().order_by('-id')[:6]
    question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        content = request.POST.get('question')
        comm = Question.objects.create(eleve_id=request.user.eleve,question = content)
        comm.save()
        return redirect('page_eleve')
    else :
        question_form = QuestionForm()


    context = {'Document':d, 'question':question_form, 'q':qst}
    return render(request, 'ged_app/homepage.html', context)




# se déconnecter
def deconnecter(request):
    logout(request)
    return redirect('connecter')




#page d'accueil pour l'admin
@login_required(login_url='connecter')
@compte_autorise
def page(request):
    context = {}
    return render(request, 'ged_app/accueil.html', context)




#Parametres du compte
@login_required(login_url='connecter')
@allowed_users(allowed_roles=['Eleve'])
def user_param(request):
    eleve = request.user.eleve
    form = EleveForm(instance=eleve)

    if request.method == "POST":
        form = EleveForm(request.POST, request.FILES, instance=eleve) 
        if form.is_valid():
            form.save()
            return redirect('parametres')
    context = {'form':form}
    return render(request, 'ged_app/basic.html', context)





 


# Publier un Document
@login_required(login_url='connecter')
#@allowed_users(allowed_roles=['Eleve'])
def upload_doc(request):
    if request.method== 'POST':
        title = request.POST.get('titre')
        fichier = request.FILES.get('fichier')
        text = request.POST.get('text')
        classe_doc = request.POST.get('classe_doc')
        genie_doc  = request.POST.get('genie_doc')
        docme = Document.objects.create(author=request.user.eleve, titre=title, fichier=fichier, text=text,classe_doc=classe_doc, genie_doc=genie_doc)
        docme.save()
        return redirect('liste_doc')
       
    return render(request, 'ged_app/upload_doc.html')



#voir la liste de tous les documents
@login_required(login_url='connecter')
def liste_doc(request):
    doc = Document.objects.all()
    context = {'docs': doc}
    return render (request, 'ged_app/liste_doc.html', context)




@login_required(login_url='connecter')
def doc_tc1(request):
    doc = Document.objects.filter(classe_doc = "TC1")
    context = {'docs' : doc}
    return render (request, 'ged_app/classe/doc_tc1.html', context)



@login_required(login_url='connecter')
def doc_tc2(request):
    doc = Document.objects.filter(classe_doc = "TC2")
    context = {'docs' : doc}
    return render (request, 'ged_app/classe/doc_tc2.html', context)



@login_required(login_url='connecter')
def doc_dic1(request):
    doc = Document.objects.filter(classe_doc = "DIC1")
    context = {'docs' : doc}
    return render (request, 'ged_app/classe/doc_dic1.html', context)



@login_required(login_url='connecter')
def doc_dic2(request):
    doc = Document.objects.filter(classe_doc = "DIC2")
    context = {'docs' : doc}
    return render (request, 'ged_app/classe/doc_dic2.html', context)



@login_required(login_url='connecter')
def doc_dic3(request):
    doc = Document.objects.filter(classe_doc = "DIC3")
    context = {'docs' : doc}
    return render (request, 'ged_app/classe/doc_dic3.html', context)





@login_required(login_url='connecter')
def doc_gtc(request):
    doc = Document.objects.filter(genie_doc = "Tronc Commun")
    context = {'docs' : doc}
    return render (request, 'ged_app/genie/doc_gtc.html', context)



@login_required(login_url='connecter')
def doc_git(request):
    doc = Document.objects.filter(genie_doc = "GIT")
    context = {'docs' : doc}
    return render (request, 'ged_app/genie/doc_git.html', context)



@login_required(login_url='connecter')
def doc_gc(request):
    doc = Document.objects.filter(genie_doc = "'Génie Civil")
    context = {'docs' : doc}
    return render (request, 'ged_app/genie/doc_gc.html', context)



@login_required(login_url='connecter')
def doc_gem(request):
    doc = Document.objects.filter(genie_doc = "Génie Electromécanique")
    context = {'docs' : doc}
    return render (request, 'ged_app/genie/doc_gem.html', context)




@login_required(login_url='connecter')
def comments(request, pk):
    docs = Document.objects.get(id=int(pk))
    com  = Commentaire.objects.filter(doc=docs, reply=None).order_by('-id')

    comment_form  = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('contenu')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Commentaire.objects.get(id=reply_id)
            comme = Commentaire.objects.create(doc=docs, author_id=request.user.eleve, contenu = content, reply = comment_qs)
            comme.save()
        else:
            comment_form  = CommentForm()

    context = {
        'doc':docs,
        'comments' : com,
        'comment_form':comment_form
        }
    return render (request, 'ged_app/doc_comments.html', context)




@login_required(login_url='connecter')
def question(request):
    question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        content = request.POST.get('question')
        comm = Question.objects.create(eleve_id=request.user.eleve,question = content)
        comm.save()
        return redirect('')
    else :
        question_form = QuestionForm()

    context ={'question':question_form}
    return render ( request, 'ged_app/poser_question.html', context)





@login_required(login_url='connecter')
def repondre(request, pk):
    quest = Question.objects.get(id= int(pk))
    rep = Reponse.objects.filter(q_id=quest).order_by('-id')

    rep_form = ReponseForm()
    if request.method == 'POST':
        rep_form = ReponseForm(request.POST or None)
        if rep_form.is_valid():
            contenu = request.POST.get('reponse')
            objet = Reponse.objects.create(el = request.user.eleve, q_id = quest, reponse=contenu)
            objet.save()
        else:
            rep_form = ReponseForm()

    context = {'question': quest, 'rep_form':rep_form, 'reponse':rep}
    return render(request, 'ged_app/repondre.html', context)










