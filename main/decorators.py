from functools import wraps
from django.http import HttpResponseForbidden

def has_role(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page!")
        return _wrapped_view
    return decorator
from functools import wraps
from django.http import HttpResponseForbidden

def has_role(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page!")
        return _wrapped_view
    return decorator
