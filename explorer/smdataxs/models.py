from django.db import models

class Smdatax(models.Model):
    unique_id = models.TextField()
    data = models.TextField()
    host_block = models.TextField(default=0)