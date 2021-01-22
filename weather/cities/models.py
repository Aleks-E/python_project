from django.db import models

class Cities(models.Model):
    Name = models.CharField('Город', max_length=30)
    Date_Time = models.DateField('Дата')
    Temperature = models.FloatField('Температура')
    Temperature_Min = models.FloatField('Температура минимальная')
    Temperature_Max = models.FloatField('Температура максимальная')
    Wind_Speed = models.FloatField('Скорость ветра', max_length=10)
    Wind_Direction = models.FloatField('Направление ветра', max_length=10)
    Precipitation = models.FloatField('Осадки', max_length=10)
    Weather_Type = models.TextField('Тип погоды')
    Conditions = models.TextField('Условия')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'




