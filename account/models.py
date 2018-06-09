from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    """Profil użytkownika, powiązany z User."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_image',blank=True)
    
    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)
    
