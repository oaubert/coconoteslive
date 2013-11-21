from gettext import gettext as _
from django.db import models

class Annotation(models.Model):
    data = models.TextField(_('Annotation data'),
                            blank=True)

    created = models.DateTimeField(_('Creation date'),
                                   help_text=_('Annotation creation date'),
                                   null=True, editable=False,
                                   auto_now_add=True)

    creator = models.CharField(_("Creator"),
                               max_length=128,
                               blank=True)

    begin = models.DateTimeField(_('Annotation begin'),
                                   help_text=_('Annotation begin'),
                                   null=True, editable=True)
    
    end = models.DateTimeField(_('Annotation end'),
                               help_text=_('Annotation end'),
                               null=True, editable=True)
    
    category = models.CharField(_('Category'),
                                max_length=128,
                                blank=True)

    source = models.CharField(_("Source"),
                               max_length=128,
                               blank=True)
