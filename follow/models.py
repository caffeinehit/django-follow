from django.db import models

from django.contrib.auth.models import User
from django.conf import settings

from util import model_map

class FollowManager(models.Manager):
    def create(self, user, obj, **kwargs):
        """
        Create a new follow link between a user and an object
        of a registered model type.
        
        """
        follow = super(FollowManager, self).create(follower=user, **kwargs)

        rel_name, f_name, m2m = model_map[obj.__class__]
        if m2m:
            field = getattr(follow, f_name)
            field.add(obj)
        else:
            setattr(follow, f_name, obj)
        follow.save()
        return follow

    def is_user_following(self, user, obj):
        """ Returns `True` or `False` """
        return user in self.get_followers_for_object(obj)

    def get_or_create(self, user, obj, **kwargs):
        """ 
        Almost the same as `FollowManager.objects.create` - behaves the same 
        as the normal `get_or_create` methods in django though. 

        Returns a tuple with the `Follow` and either `True` or `False`

        """
        if not self.is_user_following(user, obj):
            return self.create(user, obj, **kwargs), True

        return self.get_object(user, obj, **kwargs), False

    def get_object(self, user, obj, **kwargs):
        """
        Returns the `Follow` object for a regular model object.

            Follow.objects.get(user, random_object)
            -> <Follow: random_object>
        """
        rel_name, f_name, m2m = model_map[obj.__class__]
        kwargs.update({f_name: obj})
        return self.filter(**kwargs).get(follower=user)

    def get_followers_for_model(self, model):
        """
        Returns all the followers for a given model

        """
        rel_name, f_name, m2m = model_map[model]
        kwargs = {f_name: None}
        return User.objects.filter(following__in=self.exclude(**kwargs)).distinct()

    def get_followers_for_object(self, obj):
        """
        When given an object (of any type but must have been previously registered), it returns a queryset
        containing all the users following that object
        """
        rel_name, f_name, m2m = model_map[obj.__class__]
        kwargs = {f_name: obj}
        return User.objects.filter(following__in=self.filter(**kwargs)).distinct()

    def get_models_user_follows(self, user):
        """
        Returns all the model classes a user follows.
        """
        model_list = []
        for model, (rel_name, f_name, m2m) in model_map.iteritems():
            kwargs = {f_name: None}
            if Follow.objects.filter(follower=user).exclude(**kwargs):
                model_list.append(model)
        return model_list

    def get_objects_user_follows(self, user, models):
        """
        Returns all the objects a user follows from a list of models
        """
        kwargs = {}
        if isinstance(models, list):
            for model in models:
                rel_name, f_name, m2m = model_map[model]
                kwargs[f_name] = None
        else:
            rel_name, f_name, m2m = model_map[models]
            kwargs[f_name] = None
        return self.exclude(**kwargs).filter(follower=user)

    def get_everything_user_follows(self, user):
        """
        Return everythign a user follows.            
        """
        return self.filter(follower=user)

class Follow(models.Model):
    """
    This model allows a user to follow any kind of object
    """
    follower = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='following',
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
    )

    objects = FollowManager()

    def __unicode__(self):
        return '%s' % self.get_object()

    def get_object(self):
        for model, (rel_name, f_name, m2m) in model_map.iteritems():
            if hasattr(self, f_name) and getattr(self, f_name):
                return getattr(self, f_name)


