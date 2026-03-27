from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    todos = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'todos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_todos(self, obj):
        return list(obj.todo_set.values('id', 'title', 'status'))


class NoteMinimalSerializer(serializers.ModelSerializer):
    """Lightweight representation used when embedded inside a Todo."""
    class Meta:
        model = Note
        fields = ['id', 'title']
