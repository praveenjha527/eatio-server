from django.db import models


class Contact(models.Model):
    """
    The message by a user is stored here
    """
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name