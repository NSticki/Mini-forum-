from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path


class DefUser(AbstractUser):
    def is_author(self, bb):
        if self.pk == bb.author.pk:
            return True
        return False
    send_messages = models.BooleanField(default=True, verbose_name='Согласие на обработку персональных данных')

    fio = models.CharField(blank=True, max_length=150, verbose_name='ФИО', null=True)
    class Meta(AbstractUser.Meta):
        pass

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

class Status(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

class Caregory(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)



class Bb(models.Model):
    title = models.CharField(blank=True, max_length=120, verbose_name='Название', null=True)
    description = models.TextField(blank=True, max_length=120, verbose_name='Описание', null=True)
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение', null=True)
    author = models.ForeignKey(DefUser, on_delete=models.CASCADE, verbose_name='Автор', default=None, null=True)
    category = models.ForeignKey(Caregory, max_length=120, on_delete=models.CASCADE, verbose_name='категория')
    status = models.ForeignKey(Status, max_length=120, on_delete=models.CASCADE, verbose_name='Статус',default=None, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявку'

    def __str__(self):
        return self.title

class AddCommentary(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Заявки')
    comment = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        verbose_name_plural = 'Комментарий'
        verbose_name = 'Комментарий'

class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Заявки')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'



