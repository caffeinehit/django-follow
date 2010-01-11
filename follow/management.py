from django.db.models import signals
from django.db import connection

try:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("follow_followed", "New follower", "You were followed by a user")
        notification.create_notice_type("follow_unfollowed", "New unfollower", "You were unfollowed by a user")
        notification.create_notice_type("follow_blocked", "Blocked", "You were blocked by a user")
        notification.create_notice_type("follow_unblocked", "Unblocked", "You were unblocked by a user")
    signals.post_syncdb.connect(create_notice_types, sender = notification)

except ImportError:
    print "Skipping creation of notice types - notification application not found"


