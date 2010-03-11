"""

*************
Coupons
*************

.. automodule:: follow
    :members:
    :undoc-members:
    :show-inheritance:

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


def follow(user, follower):
    follow, created = Follow.objects.get_or_create(user=user, follower=follower)
    if follow.deleted:
        follow.deleted = False
        follow.save()
    return follow

def unfollow(user, follower):
    try:
        follow = Follow.objects.get(user=user, follower=follower)
    except Follow.DoesNotExist:
        return None
    follow.delete()
    return follow

def block(user, follower, blocked=True):
    try:
        follow = Follow.objects.get(user=user, follower=follower)
    except Follow.DoesNotExist:
        return None
    follow.block_user(blocked)
    follow.save()
    return follow

def unblock (user, follower):
    return block(user, follower, blocked=False)
