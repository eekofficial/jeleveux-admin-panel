from django.db import models

# Create your models here.

class Good(models.Model):
    cpa = models.TextField()
    vk_message = models.TextField(blank=True, null=True)
    tg_message = models.TextField(blank=True, null=True)
    vk = models.TextField(blank=True, null=True)
    tg = models.TextField(blank=True, null=True)
    vk_photo = models.TextField(blank=True, null=True)
    tg_photo = models.TextField(blank=True, null=True)

