from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.urls import reverse
from blogs.views import last_posts
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
        
def user_login(request):
    """Uwierzytelnienie użytkownika (logowanie)."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogs:blogs'))
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('blogs:blogs'))
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return render(request,'account/fail.html', {}) #Tu dodać template do złych danych 
        
    else:
        form = LoginForm()
    lp = last_posts()
    context = {'form': form, 'last_posts': lp}
    return render(request, 'account/login.html', context)


def logout_view(request):
    """Wylogowanie użytkownika."""
    try:
        logout(request)
    except:
        print('Blad!')
    return HttpResponseRedirect(reverse('blogs:start'))
    
    
def password_change(request):
    """Zmiana hasła do konta użytkownika."""
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account:user_login'))
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('blogs:start'))
    else:
        form = PasswordChangeForm(user=request.user)
    
    lp = last_posts()
    context = {'form': form, 'last_posts': lp}
    return render(request, 'account/change_password.html', context)
    
def register(request):
    """Rejestracja nowego użytkownika."""
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blogs:start'))
    lp = last_posts()   
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            context = {'new_user': new_user, 'last_posts': lp}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
    
    context = {'user_form': user_form, 'last_posts': lp}
    return render(request, 'account/register.html', context)

@login_required
def edit_profile(request):
    """Edytowanie profilu użytkownika."""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
     
    lp = last_posts()
    context = {'user_form': user_form, 'profile_form': profile_form, 'last_posts': lp}
    return render(request, 'account/edit_profile.html',context)

@login_required
def user_profile(request,user_id):
    """Wyświetlenie profilu użytkownika (danych podstawowych)."""
    _user = get_object_or_404(User,id=user_id)
    _profile = get_object_or_404(Profile, user=_user)
    
    lp = last_posts()
    context = {'user': _user, 'profile': _profile, 'last_posts': lp}
    return render(request, 'account/user_profile.html', context)

def error404(request):
    return render(request,'account/404.html', {})

def error500(request):
    return render(request,'account/500.html', {})
