from django.db import models
from accounts.models import CustomUser
from notes.models import Note


class FlashcardDeck(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="flashcard_decks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    source_note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deck: {self.title} ({self.user.username})"


class Flashcard(models.Model):
    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name="cards")
    front_text = models.TextField()
    back_text = models.TextField()
    hint = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card in {self.deck.title}"


class FlashcardReviewLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reviewed card {self.flashcard.id}"
