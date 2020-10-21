from django.conf import settings
from django.db import models


class Music(models.Model):
    music_id = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    gen_date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=1000)
    emotion = models.CharField(max_length=20)
    # TODO: Instruments?
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
