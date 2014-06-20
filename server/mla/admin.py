from django.contrib import admin
from .models import Group, Annotation

admin.site.register(Group)

class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'creator', 'data', 'category', 'begin', 'created', 'source', 'group')
    list_editable = ( 'creator', 'data', 'category', 'begin', 'source', 'group')
    list_display_links = ( 'pk', )

admin.site.register(Annotation, AnnotationAdmin)
