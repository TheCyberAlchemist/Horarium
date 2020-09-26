from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(next_fun):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            page = get_home_page(request.user)
            if page:
                return redirect(page)
        else:
            return next_fun(request,*args,**kwargs)
    return wrapper_function

def get_home_page(user):
    if user.groups.all():
        if str(user.groups.all()[0]) == 'Admin':
            return 'admin_home'
        elif str(user.groups.all()[0]) == 'Root':
            return 'admin_home'
        elif str(user.groups.all()[0]) == 'Student':
            return 'admin_home'
        elif str(user.groups.all()[0]) == 'Faculty':
            return 'admin_home'
    else:
        return False