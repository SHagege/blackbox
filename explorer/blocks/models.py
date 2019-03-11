from django.db import models

# Create your models here.

class BlockModel(models.Model):
    block_height = models.TextField()
    block_hash = models.TextField()
    timestamp = models.TextField()