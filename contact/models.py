from django.db import models


class Contact(models.Model):
    """ Подписка на рассылку """

    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'