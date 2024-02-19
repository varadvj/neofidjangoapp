from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    shared_users = models.ManyToManyField(User, related_name='shared_notes', blank=True)

    def __str__(self):
        return self.title

class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='version_history')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.id} of {self.note.title}"