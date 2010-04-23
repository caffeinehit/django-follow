from django import template
from django.core.urlresolvers import reverse
from follow.models import Follow
import re

register = template.Library()

def _follow_link(object):
    return reverse('follow', args=[object._meta.app_label, object._meta.object_name.lower(), object.pk])

def _unfollow_link(object):
    return reverse('unfollow', args=[object._meta.app_label, object._meta.object_name.lower(), object.pk])

@register.tag
def follow_url(parser, token):
    """
    Returns either a link to follow or to unfollow.
    
    Usage::
        
        {% follow_url object %}
        
    """
    
    try:
        tag, obj = token.split_contents()
    except:
        raise template.TemplateSyntaxError("The ``follow_link`` tag requires exactly one argument.")
    return FollowLinkNode(obj)

class FollowLinkNode(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)
        
    def render(self, context):
        obj = self.obj.resolve(context)
        
        try:
            request = context['request']
        except KeyError:
            raise template.TemplateSyntaxError('There is no request object in the template context.')
        
        if Follow.objects.is_user_following(request.user, obj):
            return _unfollow_link(obj)
        else:
            return _follow_link(obj)
        
@register.tag
def follow_class(parser, token):
    """
    Checks if the user follows a given object and then returns one of two
    specified arguments.
    
    Usage::
        
        {% follow_class object "followed" "unfollowed" %}
        
    """
    
    try:
        bits = token.split_contents()
    except:
        raise template.TemplateSyntaxError("The ``follow_class`` tag requires two or three arguments.")
    return FollowClassNode(*bits[1:])

class FollowClassNode(template.Node):
    def __init__(self, obj, followed, unfollowed=''):
        self.obj = template.Variable(obj)
        
        self.followed = re.subn('(^("|\')|("|\')$)', '', followed)[0]
        self.unfollowed = re.subn('(^("|\')|("|\')$)', '', unfollowed)[0]
        
    def render(self, context):
        obj = self.obj.resolve(context)
        
        try:
            request = context['request']
        except KeyError:
            raise template.TemplateSyntaxError('There is no request object in the template context.')
        
        if Follow.objects.is_user_following(request.user, obj):
            return self.followed
        else:
            return self.unfollowed
        
