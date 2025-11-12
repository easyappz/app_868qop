from django.db import models
from django.utils import timezone


class Member(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=32, unique=True)
    about = models.TextField(blank=True, default="")
    password_hash = models.CharField(max_length=256)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Listing(models.Model):
    CATEGORY_AUTOMOBILES = "automobiles"
    CATEGORY_PHONES = "phones"
    CATEGORY_REALTY = "realty"

    CATEGORY_CHOICES = [
        (CATEGORY_AUTOMOBILES, "Автомобили"),
        (CATEGORY_PHONES, "Телефоны"),
        (CATEGORY_REALTY, "Недвижимость"),
    ]

    author = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    images = models.JSONField(default=list, blank=True)
    phone = models.CharField(max_length=32)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["category", "created_at"]),
            models.Index(fields=["price"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.category}"


class ChatThread(models.Model):
    # Optional link to listing to indicate the chat context
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True, related_name="threads")
    member_a = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="threads_as_a")
    member_b = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="threads_as_b")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("member_a", "member_b", "listing")
        indexes = [
            models.Index(fields=["member_a", "member_b"]),
        ]

    def __str__(self):
        return f"Thread {self.id} ({self.member_a_id}-{self.member_b_id})"


class Message(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["thread", "created_at"]),
        ]

    def __str__(self):
        return f"Msg {self.id} by {self.sender_id}"
