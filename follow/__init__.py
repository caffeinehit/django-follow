"""

*************
Follow
*************

====================
Management
====================


.. automodule:: follow.management
    :members:
    :undoc-members:
    :show-inheritance:
    
====================
Models
====================
    
.. automodule:: follow.models
    :members:
    :undoc-members:
    :show-inheritance:
    
====================
Views
====================    

.. automodule:: follow.views
    :members:
    :undoc-members:
    :show-inheritance:


"""

from models import Follow

def follow(follower, obj):
    follow, created = Follow.objects.get_or_create(user=follower, obj=obj)
    return follow

def unfollow(follower, obj):
    try:
        follow = Follow.objects.get_object(user=follower, obj=obj)
    except Follow.DoesNotExist:
        return None
    follow.delete()
    return follow
