# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import smart_unicode

class GeoTag(models.Model):
    user = models.ForeignKey(User)

    lat = models.FloatField(db_index=True)
    lon = models.FloatField(db_index=True)
    zoom = models.IntegerField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    created = models.DateTimeField(db_index=True, auto_now_add=True)
    
    def __unicode__(self):
        return u"(%f,%f)" % (self.lat, self.lon)
    
    class Meta:
        unique_together = (("object_id", "content_type"),)

    @models.permalink
    def get_absolute_url(self):
        return ('geotag', (smart_unicode(self.id),))