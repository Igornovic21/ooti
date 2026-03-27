from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from notes.models import Note
from notes.serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.prefetch_related('todo_set')
    serializer_class = NoteSerializer

    @action(detail=True, methods=['get'], url_path='todos')
    def todos(self, request, pk=None):
        note = self.get_object()
        todos = note.todo_set.all()
        
        from todos.serializers import TodoSerializer
        serializer = TodoSerializer(todos, many=True, context={'request': request})
        return Response(serializer.data)
