from django import template
from django.contrib.auth.models import User, AnonymousUser, Group
from django.core.urlresolvers import reverse
from django.test import TestCase
from follow import signals, utils
from follow.models import Follow
from follow.utils import register

register(User)
register(Group)

class FollowTest(TestCase):
    urls = 'follow.urls'

    def setUp(self):
        
        self.lennon = User.objects.create(username='lennon')
        self.lennon.set_password('test')
        self.lennon.save()
        self.hendrix = User.objects.create(username='hendrix')
        
        self.musicians = Group.objects.create()
        
        self.lennon.groups.add(self.musicians)        
    
    def test_follow(self):
        follow = Follow.objects.create(self.lennon, self.hendrix)
        
        _, result = Follow.objects.get_or_create(self.lennon, self.hendrix)
        self.assertEqual(False, result)
        
        result = Follow.objects.is_following(self.lennon, self.hendrix)
        self.assertEqual(True, result)
        
        result = Follow.objects.is_following(self.hendrix, self.lennon)
        self.assertEqual(False, result)

        result = Follow.objects.get_follows(User)
        self.assertEqual(1, len(result))
        self.assertEqual(self.lennon, result[0].user)
        
        result = Follow.objects.get_follows(self.hendrix)
        self.assertEqual(1, len(result))
        self.assertEqual(self.lennon, result[0].user)
        
        result = self.hendrix.get_follows()
        self.assertEqual(1, len(result))
        self.assertEqual(self.lennon, result[0].user)
        
        result = self.lennon.get_follows()
        self.assertEqual(0, len(result), result)
        
        utils.toggle(self.lennon, self.hendrix)
        self.assertEqual(0, len(self.hendrix.get_follows()))
        
        utils.toggle(self.lennon, self.hendrix)
        self.assertEqual(1, len(self.hendrix.get_follows()))
        
    def test_get_follows_for_queryset(self):
        utils.follow(self.hendrix, self.lennon)
        utils.follow(self.lennon, self.hendrix)
        
        result = Follow.objects.get_follows(User.objects.all())
        self.assertEqual(2, result.count())
    
    def test_follow_http(self):
        self.client.login(username='lennon', password='test')
        
        follow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        unfollow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        toggle_url = reverse('toggle', args=['auth', 'user', self.hendrix.id])

        response = self.client.post(follow_url)
        self.assertEqual(302, response.status_code)
        
        response = self.client.post(follow_url)
        self.assertEqual(302, response.status_code)
        
        response = self.client.post(unfollow_url)
        self.assertEqual(302, response.status_code)
        
        response = self.client.post(toggle_url)
        self.assertEqual(302, response.status_code)
    
    def test_get_fail(self):
        self.client.login(username='lennon', password='test')
        follow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        unfollow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        
        response = self.client.get(follow_url)
        self.assertEqual(400, response.status_code)
        
        response = self.client.get(unfollow_url)
        self.assertEqual(400, response.status_code)
        
    def test_no_absolute_url(self):
        self.client.login(username='lennon', password='test')

        get_absolute_url = User.get_absolute_url
        User.get_absolute_url = None

        follow_url = utils.follow_link(self.hendrix)

        response = self.client.post(follow_url)
        self.assertEqual(500, response.status_code)

    def test_template_tags(self):
        follow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        unfollow_url = reverse('unfollow', args=['auth', 'user', self.hendrix.id])
        
        request = type('Request', (object,), {'user': self.lennon})()
        
        self.assertEqual(follow_url, utils.follow_link(self.hendrix))
        self.assertEqual(unfollow_url, utils.unfollow_link(self.hendrix))
        
        tpl = template.Template("""{% load follow_tags %}{% follow_url obj %}""")
        ctx = template.Context({
            'obj':self.hendrix,
            'request': request
        })
        
        self.assertEqual(follow_url, tpl.render(ctx))
        
        utils.follow(self.lennon, self.hendrix)
        
        self.assertEqual(unfollow_url, tpl.render(ctx))
        
        utils.unfollow(self.lennon, self.hendrix)
        
        self.assertEqual(follow_url, tpl.render(ctx))
        
        tpl = template.Template("""{% load follow_tags %}{% follow_url obj user %}""")
        ctx2 = template.Context({
            'obj': self.lennon,
            'user': self.hendrix,
            'request': request
        })
        
        self.assertEqual(utils.follow_url(self.hendrix, self.lennon), tpl.render(ctx2))
        
        tpl = template.Template("""{% load follow_tags %}{% if request.user|is_following:obj %}True{% else %}False{% endif %}""")
        
        self.assertEqual("False", tpl.render(ctx))
        
        utils.follow(self.lennon, self.hendrix)
        
        self.assertEqual("True", tpl.render(ctx))
        
        tpl = template.Template("""{% load follow_tags %}{% follow_form obj %}""")
        self.assertEqual(True, isinstance(tpl.render(ctx), unicode))
        
        tpl = template.Template("""{% load follow_tags %}{% follow_form obj "follow/form.html" %}""")
        self.assertEqual(True, isinstance(tpl.render(ctx), unicode))

    def test_signals(self):
        Handler = type('Handler', (object,), {
            'inc': lambda self: setattr(self, 'i', getattr(self, 'i') + 1),
            'i': 0
        })
        user_handler = Handler()
        group_handler = Handler()
        
        def follow_handler(sender, user, target, instance, **kwargs):
            self.assertEqual(sender, User)
            self.assertEqual(self.lennon, user)
            self.assertEqual(self.hendrix, target)
            self.assertEqual(True, isinstance(instance, Follow))
            user_handler.inc()
        
        def unfollow_handler(sender, user, target, instance, **kwargs):
            self.assertEqual(sender, User)
            self.assertEqual(self.lennon, user)
            self.assertEqual(self.hendrix, target)
            self.assertEqual(True, isinstance(instance, Follow))
            user_handler.inc()
        
        def group_follow_handler(sender, **kwargs):
            self.assertEqual(sender, Group)
            group_handler.inc()        
        
        def group_unfollow_handler(sender, **kwargs):
            self.assertEqual(sender, Group)
            group_handler.inc()
        
        signals.followed.connect(follow_handler, sender=User, dispatch_uid='userfollow')
        signals.unfollowed.connect(unfollow_handler, sender=User, dispatch_uid='userunfollow')
        
        signals.followed.connect(group_follow_handler, sender=Group, dispatch_uid='groupfollow')
        signals.unfollowed.connect(group_unfollow_handler, sender=Group, dispatch_uid='groupunfollow')
        
        utils.follow(self.lennon, self.hendrix)
        utils.unfollow(self.lennon, self.hendrix)
        self.assertEqual(2, user_handler.i)
        
        utils.follow(self.lennon, self.musicians)
        utils.unfollow(self.lennon, self.musicians)
        
        self.assertEqual(2, user_handler.i)
        self.assertEqual(2, group_handler.i)

    def test_anonymous_is_following(self):
        self.assertEqual(False, Follow.objects.is_following(AnonymousUser(), self.lennon))

    

