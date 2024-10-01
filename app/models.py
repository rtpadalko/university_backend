from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Specialization(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    budget_place = models.IntegerField(blank=True, null=True)
    budget_passing_score = models.IntegerField(blank=True, null=True)
    paid_place = models.IntegerField(blank=True, null=True)
    space_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
        db_table = "specializations"


class Applicant(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    name = models.CharField(blank=True, null=True)
    birthday_date = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Абитуриент №" + str(self.pk)

    class Meta:
        verbose_name = "Абитуриент"
        verbose_name_plural = "Абитуриенты"
        ordering = ('-date_formation', )
        db_table = "applicants"


class SpecializationApplicant(models.Model):
    specialization = models.ForeignKey(Specialization, models.DO_NOTHING, blank=True, null=True)
    applicant = models.ForeignKey(Applicant, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "specialization_applicant"
