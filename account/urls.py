from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'account'
urlpatterns = [

#    path('',views.start,name='start'),
    path('login', views.user_login,name='user_login'),
    path('logout',views.logout_view,name='logout'),
    path('change-password', views.password_change, name='password_change'),
    path('register', views.register, name='register'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('<int:user_id>/profile', views.user_profile,name='user_profile'),
    url(r'^password-reset/$', auth_views.password_reset,{'template_name': 'password_reset_form.html'}, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done,{'template_name': 'password_reset_done.html'}, name= 'password_reset_done'),
	url(r'^reset/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,{'template_name': 'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$',auth_views.password_reset_complete,{'template_name': 'password_reset_complete.html'},name='password_reset_complete'),
    path('error',views.error404,name='error404)')

    
]

