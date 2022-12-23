from django.db import models
import uuid


class Pets(models.Model):
    CHOICES = [
        ("dog", "Собака"),
        ("cat", "Кот"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, max_length=100)
    age = models.IntegerField(null=False)
    type = models.CharField(choices=CHOICES, null=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Photos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet_id = models.ForeignKey(
        "Pets", on_delete=models.SET_NULL, null=True
    )  # models.UUIDField(editable=False, null=False, db_index=True)
    url = models.TextField(max_length=1000, null=True)
    image = models.ImageField(upload_to='photo_storage/')

    def __str__(self):
        return str(self.id)
