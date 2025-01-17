from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, verbose_name="Description", blank=True)
    image = models.ImageField(blank=True, null=True, verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Vérifie si une nouvelle image a été ajoutée
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            if old_ticket.image and old_ticket.image != self.image:
                # Suppression de l'ancienne image
                old_ticket.image.delete(save=False)
        super().save(*args, **kwargs)


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
