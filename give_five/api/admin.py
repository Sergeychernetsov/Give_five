from django.contrib import admin

from .models import Documentation


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('key', 'description',)
    list_editable = ('description', )
