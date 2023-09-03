from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """ Category model. """

    name = models.CharField(
        max_length=128,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Task(models.Model):
    """ Task model. """

    title = models.CharField(
        max_length=128,
    )
    description = models.TextField(
        blank=True,
    )
    created_at = models.DateField(
        auto_now_add=True,
    )
    due_date = models.DateField(
        default=timezone.now,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    file = models.FileField(
        upload_to='tasks/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
