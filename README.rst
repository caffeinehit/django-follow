django-follow
=============

django-follow enables your users to follow any model in your Django
application.

Installation:
-------------

::

    pip install django-follow

Usage:
------

-  Add ``follow`` to your ``INSTALLED_APPS``
-  Include ``follow.urls`` into your URLs if you plan on using the
   views:

   ::

       urlpatterns = patterns('',
           url('^', include('follow.urls')),
       )

-  Register the models you want to be able to follow in your
   ``models.py`` files:

   ::

       from django.db import models
       from follow import utils

       class MyModel(models.Model):
           field = models.CharField(max_length = 255)


       utils.register(MyModel)

Test
----

The repository includes a sample project and application that is
configured to test ``django-follow``.

Clone the repository and cd into the project folder:

::

    cd test_project/
    python manage.py test follow

API
---

Manager
~~~~~~~

-  ``FollowManager.create(user, obj, **kwargs)``:
    Makes ``user`` follow ``obj``

-  ``FollowManager.get_or_create(user, obj, **kwargs)``:
    Returns a tuple ``(Follow, bool)``

-  ``FollowManager.is_following(user, obj)``:
    Returns ``bool``

-  ``FollowManager.get_follows(model_or_object)``:
    Returns all the ``Follow`` objects associated with a certain model
   or object.

Utils
~~~~~

-  ``follow.utils.register(model, field_name, related_name, lookup_method_name)``:
    Registers ``model`` to django-follow.

-  ``follow.utils.follow(user, object)``:
    Makes ``user`` follow ``object``

-  ``follow.utils.unfollow(user, object)``:
    Makes ``user`` unfollow ``object``

-  ``follow.utils.follow_url(user, object)``:
    Returns the right follow/unfollow URL for ``user`` and ``object``

-  ``follow.utils.follow_link(object)``:
    Returns the following URL for ``object``

-  ``follow.utils.unfollow_link(object)``:
    Returns the unfollowing URL for ``object``

Template Tags
~~~~~~~~~~~~~

django-follow ships a template tag that creates urls and one filter to
check if a user follows an object:

::

    {% load follow_tags %}
    {% follow_url object %}
    {% request.user|is_following:object %}

-  ``{% follow_url object %}``:
    Returns the URL to either follow or unfollow the object, depending
   on whether ``request.user`` is already following the object.

-  ``{% follow_url object other_user %}``:
    Same as above - but instead of resolving for ``request.user`` it
   resolves for any user you pass in.

-  ``{% request.user|is_following:object %}``:
    Returns ``True``/``False`` if the user follows / does not follow the
   object.

Signals
~~~~~~~

django-follow provides two signals:

-  ``follow.signals.followed(sender, user, target, instance)``
-  ``follow.signals.unfollowed(sender, user, target, instance)``

Release Notes
-------------

v0.4 - *BACKWARDS INCOMPATIBLE*

-  Made the manager *a lot* lighter.
-  Removed ``Model.followers`` method
-  Added ``Model.get_follows`` method returning all the ``Follow``
   objects
-  Moved ``Follow.follower`` to ``Follow.user``
-  Replaced ``Follow.get_object`` method with read/writable
   ``Follow.target`` property
-  ``follow.util`` moved to ``follow.utils``
-  No more M2M following

--------------

`@flashingpumpkin <http://twitter.com/flashingpumpkin>`_
