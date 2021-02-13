from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout

################ returns home if logged in or login if not #################

def unauthenticated_user(next_fun):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            page = get_home_page(request.user)
            if page:
                return redirect(page)
        else:
            return next_fun(request,*args,**kwargs)
    return wrapper_function


################ returns home page #################
def get_home_page(user):
    if user.groups.all():
        if str(user.groups.all()[0]) == 'Admin':
            return 'admin_home'
        elif str(user.groups.all()[0]) == 'Root':
            return 'root_home'
        elif str(user.groups.all()[0]) == 'Student':
            return 'student_home'
        elif str(user.groups.all()[0]) == 'Faculty':
            return 'faculty_home'
    else:
        return False


################ returns home if logged in or login if not #################
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            user_groups_set = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
                user_groups_set = set()
                for group in groups:
                    user_groups_set.add(group.name)
            allowed_roles_set = set(allowed_roles)
            if user_groups_set & allowed_roles_set:
                return view_func(request,*args,**kwargs)
            else:
                logout(request)
                return redirect('login')
                # return HttpResponse("hii")
        return wrapper_func
    return decorator