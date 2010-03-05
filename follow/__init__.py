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
