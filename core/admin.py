from django.contrib import admin
from .models import NewsletterSubscriber, BlogPost, ContactMessage

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

admin.site.register(NewsletterSubscriber)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
