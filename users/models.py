from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = 'Местоположение'

    def __str__(self):
        return self.name


class User(models.Model):
    STATUS = [
        ("member", "Гость"),
        ("moderator", "Модератор"),
        ("admin", "Администратор")
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=9, choices=STATUS, default="member")
    age = models.PositiveSmallIntegerField()
    location = models.ManyToManyField(Location)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username