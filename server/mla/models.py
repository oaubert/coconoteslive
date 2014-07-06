# -*- coding: utf-8 -*-

from gettext import gettext as _
from django.db import models

class Group(models.Model):
    class Meta:
        verbose_name_plural = "groupes"
        verbose_name = "groupe"
        ordering = ('name', 'label')

    name = models.CharField(_("Identifier"),
                            max_length=128,
                            unique=True,
                            blank=False)
    label = models.CharField(_("Label"),
                             max_length=128,
                             blank=True)

    def __unicode__(self):
        if self.label:
            return u"%s: %s" % (self.name, self.label)
        else:
            return self.name

class Annotation(models.Model):
    class Meta:
        verbose_name_plural = "annotations"
        verbose_name = "annotation"
        ordering = ('created', 'creator')

    data = models.TextField(_('Annotation data'),
                            blank=True)

    created = models.DateTimeField(_('Creation date'),
                                   help_text=_('Annotation creation date'),
                                   null=True, editable=True,
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

    group = models.ForeignKey(Group,
                              verbose_name="group",
                              related_name='items')

    def __unicode__(self):
        return "[%s:%s:%s] %s" % (self.creator,
                                  self.category,
                                  self.begin,
                                  self.data)

class Shortcut(models.Model):
    class Meta:
        verbose_name_plural = "shortcuts"
        verbose_name = "shortcut"
        ordering = ('position', 'label')

    group = models.CharField("Groupe",
                             max_length=64,
                             blank=False)
    identifier = models.CharField("Identificateur",
                                  max_length=64,
                                  unique=True,
                                  blank=True)
    label = models.CharField("Label",
                             max_length=64,
                             blank=True)
    tooltip = models.CharField("Tooltip",
                               max_length=250,
                               blank=True)
    color = models.CharField("Couleur",
                             max_length=12,
                             blank=True)
    position = models.IntegerField("Position",
                                   null=True)

    def __unicode__(self):
        return "%(identifier)s [%(group)s] %(tooltip)s (%(color)s)" % self.__dict__
