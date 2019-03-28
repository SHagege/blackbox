import json
from django.db import models
from django.template.defaultfilters import slugify

class BlockModel(models.Model):
    block_height = models.TextField(default=0)
    block_hash = models.TextField(default=0)
    block_size = models.TextField(default=0)
    timestamp = models.TextField(default=0)
    smdatax_count = models.TextField(default=0)
    slug = models.SlugField(unique=True)

    def slug(self, *args, **kwargs):
        self.slug = slugify(self.block_hash)
        super().save(*args, **kwargs)