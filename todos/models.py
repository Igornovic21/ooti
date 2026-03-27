import uuid
from django.db import models

from globals.models.timestampable import TimestampMixin


class Todo(TimestampMixin, models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    note = models.ForeignKey(
        'notes.Note',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
