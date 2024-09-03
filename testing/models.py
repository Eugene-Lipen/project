from django.db import models
from our_school.models import User
from PIL import Image
class TestingCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name="Категория", unique=True)
    slug = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Question(models.Model):
    testing_category = models.ForeignKey(TestingCategory, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст', max_length=250)
    img = models.ImageField(upload_to='photos/test_img/', blank=True)
    num_right = models.IntegerField(verbose_name='Кол-во правильных ответов')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.__dict__)
        path=self.img

        if path == '':
            pass
        else:
            image = Image.open(self.img.path)


            if image.height > 50 or image.width > 50:
                new_img = (400, 350)
                image.thumbnail(new_img)
                image.save(self.img.path)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.CharField(verbose_name='Ответ', max_length=250)
    right = models.BooleanField(verbose_name='Правильный', default=False)

    def __str__(self):
        return self.text

class TestingPeople(models.Model):
    people = models.ForeignKey(User,on_delete=models.CASCADE)
    test = models.ForeignKey(TestingCategory, on_delete=models.CASCADE)
    attempt1 = models.IntegerField(default=-1)
    switch1 = models.BooleanField(default=False)
    attempt2 = models.IntegerField(default=-1)
    switch2 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.people)


