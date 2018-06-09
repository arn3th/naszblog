from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    """Zawiera ustawienia panelu administratora dotyczącego
        profilów użytkowników."""
    list_display = ['user', 'date_of_birth', 'photo']
    
admin.site.register(Profile, ProfileAdmin)
