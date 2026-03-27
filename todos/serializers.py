from rest_framework import serializers
from todos.models import Todo

from notes.serializers import NoteMinimalSerializer


class TodoSerializer(serializers.ModelSerializer):
    note_detail = NoteMinimalSerializer(source='note', read_only=True)
    note = serializers.PrimaryKeyRelatedField(
        queryset=__import__('notes.models', fromlist=['Note']).Note.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Todo
        fields = ['id', 'title', 'status', 'note', 'note_detail', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
