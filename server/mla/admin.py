import unicodecsv as csv
import datetime
import copy

from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import util as admin_util
from django.forms import TextInput, Textarea
from django.db import models

from .models import Group, Annotation, Shortcut

def export_model_as_csv(modeladmin, request, queryset):
    if hasattr(modeladmin, 'exportable_fields'):
        field_list = modeladmin.exportable_fields
    else:
        # Copy modeladmin.list_display to remove action_checkbox
        field_list = list(modeladmin.list_display)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s-%s-export-%s.csv' % (
        __package__.lower(),
        queryset.model.__name__.lower(),
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    writer = csv.writer(response)
    writer.writerow(
        [admin_util.label_for_field(f, queryset.model, modeladmin) for f in field_list],
    )

    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_obj, attr, value = admin_util.lookup_field(field, obj, modeladmin)
            csv_line_values.append(value)

        writer.writerow(csv_line_values)

    return response
export_model_as_csv.short_description = 'CSV export'

def migrate_reference(modeladmin, request, queryset):
    for obj in queryset:
        for group in [ 'Groupe%d' % i for i in range(1, 10) ]:
            a = copy.copy(obj)
            a.id = None
            a.group = Group.objects.get(name=group)
            a.save()
            a.created = obj.created
            a.save()
    return None
migrate_reference.short_description = 'Migrate reference annotation'

class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'label')
    list_editable = ('name', 'label')
    list_display_links = ('pk', )
admin.site.register(Group, GroupAdmin)

class AnnotationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': '2', 'cols': '20'})},
    }
    list_display = ( 'uuid', 'group', 'creator', 'creatoruuid', 'data', 'category', 'begin', 'end', 'created')
    list_editable = ( 'creator', 'data', 'category', 'group')
    list_filter = ( 'group', 'creator', 'creatoruuid', 'category', 'created', 'begin' )
    search_fields = [ 'data', 'creator' ]
    exportable_fields = ('pk', 'uuid', 'group', 'creator', 'creatoruuid', 'data', 'category', 'begin', 'end', 'created', 'source')

    fieldsets = [
        (None,      {'fields': [ ('uuid', 'creator', 'creatoruuid'), 'source' ]}),
        ("Data",    {'fields': [ ('data', 'category', 'group') ] }),
        ("Time",    {'fields': [ ('begin', 'end') ] }),
        ]

    list_display_links = ( 'uuid', )
    actions = ( export_model_as_csv, migrate_reference )

admin.site.register(Annotation, AnnotationAdmin)

class ShortcutAdmin(admin.ModelAdmin):
    list_display = ('pk', 'group', 'identifier', 'label', 'tooltip', 'color', 'position')
    list_editable = ( 'group', 'identifier', 'label', 'tooltip', 'color', 'position')
    list_display_links = ( 'pk', )
    list_filter = ( 'group', )
    search_fields = [ 'identifier', 'label', 'tooltip' ]
    actions = ( export_model_as_csv, )

admin.site.register(Shortcut, ShortcutAdmin)
