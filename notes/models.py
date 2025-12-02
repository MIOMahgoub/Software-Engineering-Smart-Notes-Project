from django.db import models
from accounts.models import CustomUser

class Tag(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        unique_together = ("name", "author")   

    def __str__(self):
        return f"{self.name} ({self.author.username})"

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notes")
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    key_points = models.JSONField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

