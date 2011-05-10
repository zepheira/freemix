from django.http import HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from functools import wraps

def is_user(fn):
    def _wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user == kwargs.get("other_user") or request.user.username == kwargs.get("username"):
                return fn(request, *args, **kwargs)
        return HttpResponseForbidden(_("You do not seem to have the "
                                       "appropriate permissions to perform "
                                       "that request."))
    _wrap.__doc__ = fn.__doc__
    _wrap.__dict__ = fn.__dict__

    return wraps(fn)(_wrap)
