from django import template
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from follow import signals
from follow import utils
from follow.models import Follow

class FollowTest(TestCase):
    def setUp(self):
        
        self.lennon = User.objects.create(username='lennon')
        self.lennon.set_password('test')
        self.lennon.save()
        self.hendrix = User.objects.create(username='hendrix')
    
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
    
    def test_follow_http(self):
        self.client.login(username='lennon', password='test')
        
        follow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])
        unfollow_url = reverse('follow', args=['auth', 'user', self.hendrix.id])

        response = self.client.get(follow_url)
        self.assertEqual(302, response.status_code)
        
        response = self.client.get(follow_url)
        self.assertEqual(302, response.status_code)
        
        response = self.client.get(unfollow_url)
        self.assertEqual(302, response.status_code)


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
        
        tpl = template.Template("""{% load follow_tags %}{{ request.user|is_following:obj }}""")
        
        self.assertEqual("False", tpl.render(ctx))
        
        utils.follow(self.lennon, self.hendrix)
        
        self.assertEqual("True", tpl.render(ctx))

    def test_signals(self):
        def follow_handler(user, target, instance, **kwargs):
            self.assertEqual(self.lennon, user)
            self.assertEqual(self.hendrix, target)
            self.assertEqual(True, isinstance(instance, Follow))
            
        signals.followed.connect(follow_handler)
        
        utils.follow(self.lennon, self.hendrix)
        
        def unfollow_handler(user, target, instance, **kwargs):
            self.assertEqual(self.lennon, user)
            self.assertEqual(self.hendrix, target)
            self.assertEqual(True, isinstance(instance, Follow))
        
        utils.unfollow(self.lennon, self.hendrix)
        
