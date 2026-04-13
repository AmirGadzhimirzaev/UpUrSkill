from django.db import models


class Lesson(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='название урока'
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.SET_NULL,
        verbose_name='курс',
        blank=True,
        null=True,
        related_name='course'
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    preview = models.ImageField(
        upload_to='materials/lesson/photo',
        blank=True,
        null=True
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='ссылка на видео'
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Владелец урока"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='название курса'
    )
    preview = models.ImageField(
        upload_to='materials/course/photo',
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Владелец урока"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
