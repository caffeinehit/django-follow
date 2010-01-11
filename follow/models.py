from django.db import models

from django.db.models import signals

from django.contrib.auth.models import User
from django.conf import settings

try:
    from notification import models as notification
except ImportError:
    notification = None

try:
    import stream
except:
    stream = None
    
FOLLOW_NOTIFICATION = getattr(settings, 'FOLLOW_NOTIFICATION', False)

class FollowManager(models.Manager):
    def get_followers(self, user):
        return self.filter(deleted=False, blocked=False, user=user).select_related()
    def get_followed(self, user):
        return self.filter(deleted=False, blocked=False, follower=user).select_related()

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='followers'
    )

    follower = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='following'
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
    )

    deleted = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )

    blocked = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )

    pre_block = None
    block = None

    objects = FollowManager()

    def __unicode__(self):
        return '%s' % self.follower.username

    def block_user(self, status):
        self.pre_block = self.blocked
        self.blocked = status
        if self.blocked and not self.pre_block: # New block
            self.block = 'add'
        if not self.blocked and self.pre_block: # Unblock
            self.block = 'del'
        else: # no change
            self.block = None

    def delete(self):
        self.deleted = True
        self.save()

def save_handler(sender, instance, created, **kwargs):
    """ Send notifications and register items in the stream :-o """
    if not created: # Handle blocks!
        if instance.block and instance.block == 'new':
            if notification and FOLLOW_NOTIFICATION:
                notification.send([instance.follower], 'follow_blocked', on_site=False)
            if stream and FOLLOW_NOTIFICATION:
                stream.add([instance.user, instance], type='follow_blocked')
        elif instance.block and instance.block == 'del':
            if notification and FOLLOW_NOTIFICATION:
                notification.send([instance.follower], 'follow_unblocked', on_site=False)
            if stream and FOLLOW_NOTIFICATION:
                stream.add([instance.user, instance], type='follow_unblocked')
        else:
            pass
        return
    if notification and FOLLOW_NOTIFICATION:
        notification.send([instance.user], 'follow_followed', on_site=False)
    if stream and FOLLOW_NOTIFICATION:
        stream.add([instance.follower, instance], type='follow_followed')

def delete_handler(sender, instance, **kwargs):
    """ Send notifications and register items in the stream """
    if notification and FOLLOW_NOTIFICATION:
        notification.send([instance.user], 'follow_unfollowed', on_site=False)
    if stream and FOLLOW_NOTIFICATION:
        stream.add([instance.follower, instance], type='follow_unfollowed')

signals.post_save.connect(save_handler, sender=Follow)
signals.post_save.connect(delete_handler, sender=Follow)

if stream:
    stream.register(Follow)

from django.contrib import admin
admin.site.register(Follow)
