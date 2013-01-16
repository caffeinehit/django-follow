# django-follow

![](https://secure.travis-ci.org/caffeinehit/django-follow.png)

django-follow enables your users to follow any model in your Django application.

## Installation:

    pip install django-follow

## Usage:

* Add `follow` to your `INSTALLED_APPS`
* Include `follow.urls` into your URLs if you plan on using the views:

		urlpatterns = patterns('',
			url('^', include('follow.urls')),
		)
	
* Register the models you want to be able to follow in your `models.py` files:

		from django.db import models
		from follow import utils

		class MyModel(models.Model):
			field = models.CharField(max_length = 255)
		

		utils.register(MyModel)

**NOTE** You must register your models before running `syncdb` or you
  will run into the issue described in [django-follow/issues/16](https://github.com/caffeinehit/django-follow/issues/16)


## Test

The repository includes a sample project and application that is configured
to test `django-follow`.

Clone the repository and cd into the project folder:

	cd example/
	python manage.py test follow
    
## API

### Manager

* `Follow.objects.create(user, obj, **kwargs)`:  
  Makes `user` follow `obj`

* `Follow.objects.get_or_create(user, obj, **kwargs)`:  
  Returns a tuple `(Follow, bool)` 

* `Follow.objects.is_following(user, obj)`:  
  Returns `bool`

* `Follow.objects.get_follows(model_or_object_or_queryset)`:  
  Returns all the `Follow` objects associated with a certain model, object or
  queryset.

**Note on performance**

I advise against against using `Follow.objects.is_following` too often in one
request / response cycle on single objects. Use it on querysets to avoid stacking
up too many queries.


### Utils

* `follow.utils.register(model, field_name, related_name, lookup_method_name)`:  
  Registers `model` to django-follow. 

* `follow.utils.follow(user, object)`:  
  Makes `user` follow `object`

* `follow.utils.unfollow(user, object)`:  
  Makes `user` unfollow `object`

* `follow.utils.toggle(user, object)`:  
  Toggles `user`'s follow status of `object`

* `follow.utils.follow_url(user, object)`:  
  Returns the right follow/unfollow URL for `user` and `object`

* `follow.utils.follow_link(object)`:  
  Returns the following URL for `object`
  
* `follow.utils.unfollow_link(object)`:  
  Returns the unfollowing URL for `object`


### Template Tags

django-follow ships a template tag that creates urls, a filter 
to check if a user follows an object and a template tag to render
the follow form.

	{% load follow_tags %}
	{% follow_url object %}
	{% request.user|is_following:object %}
	{% follow_form object %}
	{% follow_form object "your/custom/template.html" %}

* `{% follow_url object %}`:  
  Returns the URL to either follow or unfollow the object, depending on whether `request.user` is already following the object. 

* `{% follow_url object other_user %}`:  
  Same as above - but instead of resolving for `request.user` it resolves for any user you pass in.
 
* `{% request.user|is_following:object %}`:  
  Returns `True`/`False` if the user follows / does not follow the object.

* `{% follow_form object %}`:  
  Renders a form to follow a given object.

* `{% follow_form object "your/custom/template.html" %}:  
  Renders the form with a custom template.


### Signals

django-follow provides two signals:

* `follow.signals.followed(sender, user, target, instance)`
* `follow.signals.unfollowed(sender, user, target, instance)`

To invoke a handler every time a `User` or `Group` object is followed, do something along these lines:

	from django.contrib.auth.models import User
	from follow import signals

	def user_follow_handler(user, target, instance, **kwargs):
		send_mail("You were followed", "You have been followed", "no-reply@localhost", [target.email])
	
	def group_follow_handler(user, target, instance, **kwargs):
		send_mail("Group followed", "%s has followed your group" % user, "no-reply@localhost", [[u.email for u in target.user_set.all()]])

	signals.followed.connect(user_follow_handler, sender = User, dispatch_uid = 'follow.user')
	signals.followed.connect(group_follow_handler, sender = Group, dispatch_uid = 'follow.group')

This works vica versa with the unfollowed handler too.

**NOTE**

When handling `follow.signals.unfollowed` both `user` and/or `target` can be
`None`. Django's admin for example will first delete the user resulting in
`instance.user` to throw `DoesNotExist`. Beware.

## Release Notes

v0.5 - *BACKWARDS INCOMPATIBLE*

* The follow and unfollow views now only accept POST requests

v0.4 - *BACKWARDS INCOMPATIBLE*

* Made the manager _a lot_ lighter.
* Removed `Model.followers` method
* Added `Model.get_follows` method returning all the `Follow` objects
* Moved `Follow.follower` to `Follow.user` 
* Replaced `Follow.get_object` method with read/writable `Follow.target` property
* `follow.util` moved to `follow.utils`
* No more M2M following

-----------------

[@flashingpumpkin](http://twitter.com/flashingpumpkin)
