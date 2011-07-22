from django import template
from django.core.urlresolvers import reverse
from follow.models import Follow
from follow import utils
import re

register = template.Library()

@register.tag
def follow_url(parser, token):
    """
    Returns either a link to follow or to unfollow.
    
    Usage::
        
        {% follow_url object %}
        {% follow_url object user %}
        
    """
    bits = token.split_contents()
    return FollowLinkNode(*bits[1:])

class FollowLinkNode(template.Node):
    def __init__(self, obj, user=None):
        self.obj = template.Variable(obj)
        self.user = user
        
    def render(self, context):
        obj = self.obj.resolve(context)
        
        if not self.user:
            try:
                user = context['request'].user
            except KeyError:
                raise template.TemplateSyntaxError('There is no request object in the template context.')
        else:
            user = template.Variable(self.user).resolve(context)
        
        return utils.follow_url(user, obj)
        

@register.filter
def is_following(user, obj):
    """
    Returns `True` in case `user` is following `obj`, else `False`
    """
    return Follow.objects.is_following(user, obj)


