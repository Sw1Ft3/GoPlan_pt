from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """Модель расписания"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Event(models.Model):
    """Модель события в расписании"""
    DAYS_OF_WEEK = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='events', verbose_name='Расписание')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    color = models.CharField(max_length=7, default='#3b82f6', verbose_name='Цвет')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.get_day_of_week_display()}"
