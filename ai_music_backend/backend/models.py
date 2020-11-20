from django.conf import settings
from django.db import models
from django.utils import timezone


class Music(models.Model):
    music_id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=100, null=True)
    gen_date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=1000)
    emotion = models.CharField(max_length=20)
    instruments = models.IntegerField(default=0)
    # TODO: Instruments?
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.music_id
