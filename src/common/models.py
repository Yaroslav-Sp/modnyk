from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)
    edit_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
