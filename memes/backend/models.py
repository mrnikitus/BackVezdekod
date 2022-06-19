from django.contrib.auth.models import User
from django.db import models

class Meme(models.Model):
    def directory(instance, filename):
        return f'{instance.created_at.strftime("%Y-%m-%d")}/{filename}'
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    photo = models.URLField(verbose_name='Мем')
    author = models.CharField(null=True, blank=True, max_length=255,verbose_name='Автор мема')
    likes = models.PositiveIntegerField(default=0, verbose_name='Число лайков')
    important = models.BooleanField(default=False, verbose_name='Важный', help_text='Отметить, чтобы мем показывался чаще других')
    def __str__(self):
        return f'Мем №{self.id} от {self.created_at.strftime("%d.%m.%Y %H:%M")}'
    class Meta:
        verbose_name = 'мем'
        verbose_name_plural = 'мемы'

class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, verbose_name='Мем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    liked = models.BooleanField(default=True, verbose_name='Лайкнут (или пропущен)')
    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        likeMeme = Meme.objects.get(id=self.meme.id)
        likeMeme.likes = Like.objects.filter(meme=likeMeme, liked=True).count()
        likeMeme.save()

    def __str__(self):
        return f'Лайк №{self.id} на мем №{self.meme.id} от {self.created_at.strftime("%d.%m.%Y %H:%M")}'
    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'лайки'
