from django.dispatch.dispatcher import Signal

followed = Signal(providing_args=["user", "target", "instance"])
unfollowed = Signal(providing_args=["user", "target", "instance"])
