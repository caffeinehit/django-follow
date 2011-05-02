"""

>>> from django.contrib.auth.models import User, Group
>>> from follow.models import Follow

>>> flashingpumpkin = User.objects.create(username='flashingpumpkin')
>>> devioustree = User.objects.create(username='devioustree')

>>> Follow.objects.create(flashingpumpkin, devioustree)
<Follow: devioustree>

>>> Follow.objects.create(devioustree, flashingpumpkin)
<Follow: flashingpumpkin>

>>> Follow.objects.get_or_create(flashingpumpkin, devioustree)
(<Follow: devioustree>, False)

>>> Follow.objects.is_user_following(flashingpumpkin, devioustree)
True

>>> Follow.objects.get_followers_for_model(User)
[<User: flashingpumpkin>, <User: devioustree>]

>>> Follow.objects.get_followers_for_object(flashingpumpkin)
[<User: devioustree>]

>>> Follow.objects.get_models_user_follows(devioustree)
[<class 'django.contrib.auth.models.User'>]

>>> Follow.objects.get_objects_user_follows(devioustree, User)
[<Follow: flashingpumpkin>]

>>> Follow.objects.get_objects_user_follows(devioustree, [User, Group])
[<Follow: flashingpumpkin>]

>>> Follow.objects.get_everything_user_follows(devioustree)
[<Follow: flashingpumpkin>]

>>> Follow.objects.get_object(flashingpumpkin, devioustree)
<Follow: devioustree>

>>> devioustree.followers()
[<User: flashingpumpkin>]

"""


