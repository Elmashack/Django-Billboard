from django.db import models
from django.contrib.auth.models import AbstractUser


class BoardUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?')
    com_notification = models.BooleanField(default=True, verbose_name='Оповещение о новых комментариях')

    def delete(self, *args, **kwargs):
        for board in self.bboard_set.all():
            board.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass

