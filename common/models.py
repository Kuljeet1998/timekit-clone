from django.db import models
from django.utils.timezone import now
import uuid
# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True

class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    pass

    class Meta:
        abstract = True
