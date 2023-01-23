from django.contrib import admin

from .models import Theme

class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.register(Theme, ThemeAdmin)
