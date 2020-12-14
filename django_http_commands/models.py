from django.db import models


def default_storage():
    return {'args': [], 'kwargs': {}}


class ManagementCommand(models.Model):
    name = models.CharField(max_length=250, null=False, unique=True)
    app = models.CharField(max_length=250, null=False)
    expose = models.BooleanField(default=False)

    def __str__(self):
        return self.name
