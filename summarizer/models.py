# summarizer/models.py
from django.db import models

class Document(models.Model):
    document_type = models.CharField(max_length=20, choices=[('pdf', 'PDF'), ('youtube', 'YouTube')])
    content = models.TextField()
    summary = models.TextField(null=True, blank=True)
