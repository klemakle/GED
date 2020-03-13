from django.http import HttpResponse
from django.shortcuts import redirect


def nonauthentifie_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('page')
        else:
            return view_func(request, *args,**kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def mafonc(view_func):
        def wrapper_func(request, *args,**kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                return HttpResponse("Vous n'êtes pas autorisé")
        return wrapper_func
    return mafonc



def compte_autorise(view_func):
    def wrapper_func(request, *args,**kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Eleve':
            return redirect ('page_eleve')

        if group == 'admin':
            return view_func(request, *args,**kwargs)
        else:
              return redirect("page")
    return wrapper_func
   
