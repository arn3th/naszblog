from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post, Blog, Comment
from .forms import BlogForm, PostForm, CommentForm, EmailPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

def start(request):
    """Wyświetlenie napisu strony początkowej."""
    napis = 'Witaj na naszblog!'
    lp = last_posts()
    context = {'text': napis, 'last_posts': lp}
    return render(request,'blogs/index.html', context)
    
@login_required
def blogs(request):
    """Wyświetlanie wszystkich blogów użytkownika."""
    
    objects = Blog.objects.filter(owner=request.user)
    paginator = Paginator(objects,10)
    page = request.GET.get('page')
    lp = last_posts()
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
        
        
    context = {'blogs': blogs, 'page': page, 'last_posts': lp}
    return render(request, 'blogs/blogs.html', context)

def blog(request, blog_id, name):
    """Wyświetlenie listy postów na wybranym blogu."""
    blog = get_object_or_404(Blog, id=blog_id, slug=name)
    if blog.owner == request.user:
        posts = Post.objects.filter(blog=blog_id)
    else:
        posts = Post.public.filter(blog=blog_id)
    lp = last_posts()
    context = {'posts': reversed(posts), 'blog': blog, 'last_posts': lp}
    return render(request, 'blogs/blog.html', context)
    
@login_required    
def new_blog(request):
    """Dodaj nowy blog."""
    if request.method != 'POST':
        #nie przekazano danych, utwórz pusty formularz
        form = BlogForm()
    else: 
        #przekazano dane za pomocą żadania POST, należy je przetworzyć
        form = BlogForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return HttpResponseRedirect(reverse('blogs:blogs'))
    lp = last_posts()
    context = {'form': form, 'last_posts': lp}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def delete_blog(request, blog_id):
    """Usuń wybrany blog."""
    
    blog = get_object_or_404(Blog, id=blog_id)
    check_owner(request.user, blog.owner)
    lp = last_posts()
    if request.method != 'POST':
        text = 'Czy na pewno chcesz usunąć blog "{}"?'.format(blog.title)
        context = {'text': text, 'blog_id': blog.id, 'last_posts': lp}
        return render(request, 'blogs/delete.html', context) 
    else:
        blog.delete()
        return HttpResponseRedirect(reverse('blogs:blogs'))

@login_required
def new_post(request, blog_id):
    """Odpowiada za dodawanie nowego posta."""
    blog = get_object_or_404(Blog, id=blog_id)
    check_owner(request.user, blog.owner)
    
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.save()
            return HttpResponseRedirect(reverse('blogs:blog',
                                        args=[blog.id, blog.slug]))
    lp = last_posts()                                
    context = {'blog': blog, 'form': form, 'last_posts': lp}
    return render(request, 'blogs/new_post.html', context)

def post_detail(request,post_id,slug):
    """Wyświetlenie posta, jego treści, wraz z komentarzami."""
    _post = get_object_or_404(Post,id=post_id,slug=slug)
    if _post.status == 'private':
        check_owner(request.user, _post.blog.owner)
    blog = _post.blog
    
    #Lista aktywnych komentarzy dla danego posta
    comments = Comment.objects.filter(post=_post.id)
    is_new_comment = False
    
    if request.method == 'POST':
        #Komentarz został opublikowany
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #check_comment = post.comments.values_list('name','body')
            #Utworzenie obiektu Comment, ale jeszcze nie zapisujemy go w bazie danych
            new_comment = comment_form.save(commit=False)
            #Przypisanie komentarza do bieżącego posta
            new_comment.author_id = request.user.id
            new_comment.post = _post
           # if (new_comment.name, new_comment.body) in check_comment:
            #    comment_form = CommentForm()
            #Zapisanie komentarza w bazie danych
           # else:
            new_comment.save()
            is_new_comment = True
    else:
        comment_form = CommentForm()
    
    lp = last_posts()
    context = {'post':_post, 'blog': blog, 'comments': comments, 'comment_form': comment_form, 'flag': is_new_comment, 'last_posts': lp}
    return render(request,'blogs/post_detail.html', context)

@login_required
def edit_post(request,post_id):
    """Edytowanie posta."""
    
    post = get_object_or_404(Post, id=post_id)
    blog = post.blog
    check_owner(request.user, blog.owner)
    form = PostForm(request.POST,instance=post)
    
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:post_detail',
                                        args=[post.id, post.slug]))
    lp = last_posts()
    context = {'post': post, 'form': form, 'last_posts': lp}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    """Usuwanie wybranego posta."""
    
    post = get_object_or_404(Post, id=post_id)
    check_owner(request.user, post.blog.owner)
    
    if request.method != 'POST':
        text = 'Czy na pewno chcesz usunąć post "{}"?'.format(post.name)
        lp = last_posts()
        context = {'text': text, 'post': post, 'last_posts': lp}
        return render(request, 'blogs/delete_post.html', context) 
    else:
        post.delete()
        return HttpResponseRedirect(reverse('blogs:blogs'))

@login_required
def delete_comm(request, comm_id):
    """Usuwanie wybranego komentarza."""
    
    comment = get_object_or_404(Comment,id=comm_id)
    post = get_object_or_404(Post,id=int(comment.post.id))
    comment.delete()
    url = reverse('blogs:post_detail', kwargs={'post_id':post.id, 'slug':post.slug})
    return HttpResponseRedirect(url)
    
def post_share(request, post_id, slug):
    """Udostępnienie konkretnego posta za pomocą e-mail."""
    post = get_object_or_404(Post, id=post_id,status='public' )
    sent = False
    
    if request.method == 'POST':
        #Formularz wysłany
        form = EmailPostForm(request.POST) 
        #Tworzymy egzemplarz formularza na podstawie wysłanych danych
        if form.is_valid():
            cd = form.cleaned_data #Dane formularza otrzymane w postaci słownika
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} zachęca do przeczytania "{}"'.format(request.user.username,
                post.name)
            message = 'Przeczytaj post "{}" na stronie {}\n\n{}: {}'.format(post.name, post_url, request.user.username, cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['Do']])
            sent = True
            
    else:
        #Pusty formularz
        form = EmailPostForm()
    lp = last_posts()
    context = {'post': post, 'form': form, 'sent': sent, 'last_posts': lp}
    return render(request, 'blogs/share.html',context)
    
def search(request):
    """Wyszukiwanie postów zawierających wpisaną frazę."""
    query = request.GET.get('q')
    posts = Post.public.filter(
        Q(name__icontains=query) |
        Q(text__icontains=query) 
        ).distinct()
    lp = last_posts()
    context = {'posts': posts, 'last_posts': lp}
    return render(request, 'blogs/search.html', context)
    
def check_owner(user,owner):
    """Sprawdzenie uwierzytelnionego użtkownika z właścicielem."""
    if user != owner:
        raise Http404
        
def last_posts():
    """Zwraca 8 ostatnio dodanych postów."""
    last_posts = Post.public.all().order_by('-date_added')[:8]
    return last_posts;
    

