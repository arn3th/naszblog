from django import forms

from .models import Blog, Post, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title']
        labels = {'title':''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name','text','status',]
        labels = {'text':'Treść', 'name':'Tytuł'}
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
        labels = {'body':''}

class EmailPostForm(forms.Form):
    Do = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        fields = ['do','comments']
        labels = {'comments':''}

        

