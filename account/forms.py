from django import forms
from django.contrib.auth.models import User
from .models import Profile
from captcha.fields import ReCaptchaField

class LoginForm(forms.Form):
    """Formularz logowania."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    """Formularz rejestracji nowego użytkownika."""
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField()
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Hasła nie są identyczne.')
            return cd['password2']
    
class UserEditForm(forms.ModelForm):
    """Formularz edytowania danych użytkownika."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')
        
class ProfileEditForm(forms.ModelForm):
    """Formularz edytowania danych z profilu użytkownika."""
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
        labels = {'photo': 'Photo',}

