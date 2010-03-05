from follow import follow as _follow, unfollow as _unfollow

from django.contrib.auth.decorators import login_required
from django.db.models.loading import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext as _

from django.contrib.auth.models import User

def check(func):
    """ 
    Check the permissions, http method and login state
    """
    def iCheck(request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        if user == request.user:
            return HttpResponseBadRequest()
        
        func(request, user)
        return HttpResponse()
    return iCheck

@login_required
@check
def follow(request, app, model, obj):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=obj)
    _follow(request.user, obj)

@login_required
@check
def unfollow(request, app, model, obj):
    model = cache.get_model(app, model)
    obj = model.objects.get(pk=obj)
    _unfollow(request.user, obj)
