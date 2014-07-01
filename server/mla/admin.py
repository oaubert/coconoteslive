from django.contrib import admin
from .models import Group, Annotation, Shortcut

admin.site.register(Group)

class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'creator', 'data', 'category', 'begin', 'created', 'source', 'group')
    list_editable = ( 'creator', 'data', 'category', 'begin', 'source', 'group')
    list_display_links = ( 'pk', )

admin.site.register(Annotation, AnnotationAdmin)

class ShortcutAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'identifier', 'label', 'tooltip', 'color', 'position')
    list_editable = ( 'group', 'identifier', 'label', 'tooltip', 'color', 'position')
    list_display_links = ( 'pk', )

admin.site.register(Shortcut, ShortcutAdmin)
