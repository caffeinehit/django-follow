from follow import follow as _follow, unfollow as _unfollow, \
    block as _block, unblock as _unblock

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import gettext as _

from django.contrib.auth.models import User

def check(func):
    """ 
    Check the permissions, http method and login state
    """
    def iCheck(request, username):
        if not request.user.is_authenticated():
            return render_to_response(
                'follow/error.html', dict(message=_("Please log in first.")),
                context_instance=RequestContext(request)
            )
            
        if not request.is_ajax():
            return render_to_response(
                'follow/error.html', dict(message=_("Wrong method.")),
                context_instance=RequestContext(request)
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render_to_response(
                'follow/error.html', dict(message=_("Bad Username")),
                context_instance=RequestContext(request)
            )
        if user == request.user:
            return render_to_response(
                'follow/error.html', dict(message=_("You can't %s yourself." % func.__name__)),
                context_instance=RequestContext(request)
            )
        
        func(request, user)
        return render_to_response(
            'follow/success_%s.html' % func.__name__, dict(),
            context_instance=RequestContext(request)
        )
    return iCheck

@check
def follow(request, user):
    _follow(user, request.user)
    


@check
def unfollow(request, user):
    _unfollow(user, request.user)
    

@check
def block(request, user):
    _block(request.user, user)
    

@check
def unblock(request, user):
    _unblock(request.user, user)

