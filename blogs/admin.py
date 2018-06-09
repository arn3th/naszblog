from django.contrib import admin
from .models import Blog, Post, Comment

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    """Zawiera ustawienia panelu administratora dotyczącego blogów."""
    prepopulated_fields = {'slug':('title',)}
    
class PostAdmin(admin.ModelAdmin):
    """Zawiera ustawienia panelu administratora dotyczącego postów."""
    list_display = ('name','blog','status') #dodaje kolumny danych
    list_filter = ('status','blog') #dodaje możliwość filtrowania z prawej strony
    search_fields = ('name','body') #dodaje możliwość wyszukiwania w name i body
    raw_id_fields = ('blog',) #dodanie bloga po id podczas dodawania postu
    ordering = ['status'] #kolejność
    prepopulated_fields = {'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    """Zawiera ustawienia panelu administratora dotyczącego komentarzy."""
    list_display = ('author', 'body')
    list_filter = ('created', 'updated')
 
admin.site.register(Blog,BlogAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

