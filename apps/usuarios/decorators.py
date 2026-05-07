from functools import wraps
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_transito:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def agente_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_agente:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
