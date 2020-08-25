from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(next_fun):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('table')
        else:
            return next_fun(request,*args,**kwargs)
    return wrapper_function