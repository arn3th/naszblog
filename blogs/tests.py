from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import Blog, Post, Comment
from django.contrib.auth.models import User
from django.test import Client
from django.test.utils import setup_test_environment
import time as t

# Create your tests here.
def create_user(nick, password):
    user = User.objects.create(username=nick, password=password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user
    
def create_blog(title,us):
    blog = Blog.objects.create(title=title, owner=us)
    blog.save()
    return blog
    
def create_post(blog, name, text):
    post = Post.objects.create(blog=blog, name=name, text=text)
    post.save()
    return post
    
def create_comment(post,author,text):
    comment = Comment.objects.create(post=post,author=author,body=text)
    comment.save()
    
class BlogsPostsTests(TestCase):
    
    def test_no_posts(self):
        """
        Jeśli użytkownika nie dodał żadnego posta,
        lista zwróconych postów będzie pusta.
        """

        user = create_user('foo','bar')
        blog = create_blog('BlogTest',user)
        response = self.client.get(reverse('blogs:blog',
                                        args=[blog.id, blog.slug]))
        self.assertQuerysetEqual(response.context['posts'], [])
        
    def test_two_last_posts(self):
        """
        Po dodaniu dwóch postów przez użytkownika,
        zostaną one przypisane do ostatnich postów.
        """
        
        _user = create_user('fo','bar')
        _blog = create_blog('blog',_user)
        post1 = create_post(_blog,'Post1','Tresc Post 1')
        post2 = create_post(_blog,'Post2','Tresc Post 1')
        
        response = self.client.get(reverse('blogs:blog',args=[_blog.id, _blog.slug]))
        self.assertQuerysetEqual(response.context['last_posts'], ['<Post: Tresc Post 1>', '<Post: Tresc Post 1>'])
        
    def test_eight_last_posts(self):
        """
        Po dodaniu dziewięciu i więcej postów, 
        do last_posts zostanie zwrócone 8 najnowszych.
        """
        
        _user = create_user('fo','bar')
        _blog = create_blog('blog',_user)
        i = 0
        while i<9:
            create_post(_blog,'Tytuł{}'.format(str(i)),'Post{}'.format(str(i)))
            i+=1
            t.sleep(1)
        response = self.client.get(reverse('blogs:blog',args=[_blog.id, _blog.slug]))
        self.assertQuerysetEqual(response.context['last_posts'], 
                                ['<Post: Post8>', '<Post: Post7>',
                                 '<Post: Post6>', '<Post: Post5>',
                                 '<Post: Post4>', '<Post: Post3>',
                                 '<Post: Post2>', '<Post: Post1>'])
        i = 0
                                 
    def test_comments(self):
        """
        Po dodaniu komentarza, powinien pojawić się
        on pod postem.
        """
        _user = create_user('fo','bar')
        _blog = create_blog('blog',_user)
        _post = create_post(_blog,'Post11','Tresc Post 1')
        create_comment(_post,_user,'Komentarz')
        
        response = self.client.get(reverse('blogs:post_detail',args=[_post.id, _post.slug]))
        self.assertQuerysetEqual(response.context['comments'], ['<Comment: Komentarz>'])
        
    def test_send_email(self):
        """
        Dopóki funkcja nie otrzyma żądania POST,
        e-mail nie zostanie wysłany.
        """
        
        _user = create_user('fo','bar')
        _blog = create_blog('blog',_user)
        _post = create_post(_blog,'Post1','Tresc Post 1')
        response = self.client.get(reverse('blogs:post_share',args=[_post.id, _post.slug]))
        self.assertFalse(response.context['sent'])
        
        
        
        
        
