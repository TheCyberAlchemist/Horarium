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
            return 'root_home'
        elif str(user.groups.all()[0]) == 'Student':
            return 'admin_home'
        elif str(user.groups.all()[0]) == 'Faculty':
            return 'admin_home'
    else:
        return False

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                print(get_home_page(request.user))
                return redirect(get_home_page(request.user))
                # return HttpResponse("hii")
        return wrapper_func
    return decorator