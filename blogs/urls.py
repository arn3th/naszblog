from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [

    path('blogs',views.blogs,name='blogs'),
    path('new_blog',views.new_blog,name='new_blog'),
    path('<int:blog_id>/<name>/', views.blog, name='blog'),
    path('blog/delete/<int:blog_id>',views.delete_blog,name='delete_blog'),
    path('<int:blog_id>/new_post',views.new_post,name='new_post'),
    path('<int:post_id>/<slug>',views.post_detail,name='post_detail'),
    path('edit/post/<int:post_id>', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>',views.delete_post,name='delete_post'),
    path('delete/comm/<int:comm_id>',views.delete_comm,name='delete_comm'),
    path('<int:post_id>/<slug>/share',views.post_share,name='post_share'),
    path('posts/search',views.search,name='search'),
     path('',views.start,name='start'),
    
]

