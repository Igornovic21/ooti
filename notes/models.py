from django.db import models

from globals.models.timestampable import TimestampMixin


class Note(TimestampMixin, models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
