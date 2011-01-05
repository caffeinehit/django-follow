from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.loading import cache
from django.http import (HttpResponse, HttpResponseBadRequest,
    HttpResponseRedirect, HttpResponseServerError)
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _
from follow import follow as _follow, unfollow as _unfollow


def check(func):
    """ 
    Check the permissions, http method and login state
    """
    def iCheck(request, *args, **kwargs):
        follow = func(request, *args, **kwargs)
        if request.is_ajax():
            return HttpResponse('ok')
        try:
            if 'ref' in request.GET:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            return HttpResponseRedirect(follow.get_object().get_absolute_url())
        except KeyError:
            return HttpResponseServerError('No HTTP_REFERER')
        except AttributeError:
            return HttpResponseServerError('"%s" object of type ``%s`` has no method ``get_absolute_url()``.' % (
                unicode(follow.get_object()), follow.get_object().__class__))
    return iCheck


@login_required
@check
def follow(request, app, model, id):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=id)
    return _follow(request.user, obj)

@login_required
@check
def unfollow(request, app, model, id):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=id)
    return _unfollow(request.user, obj)
