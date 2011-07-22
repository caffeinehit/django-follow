from django.db import models
from django.contrib.auth.models import User, Group
from follow.utils import register

register(User)
#register(Group)


