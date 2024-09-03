import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image




# пользователи админы и личные кабинеты

class Work_Name(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = PhoneNumberField(blank=True)
    date_job = models.DateField(default=datetime.date.today())
    telegram = models.CharField(max_length=255, blank=True)
    position = models.ForeignKey(Work_Name,  on_delete=models.CASCADE, null=True)
    turn_on_test = models.BooleanField(default=False)
    point = models.FloatField(default=0)
    number_attempts = models.IntegerField(default=2)


    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username




# отображение категорий подкатегорий лекций и содержание в обучающем блоке
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Категория", unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/category', null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (300, 250)
            img.thumbnail(new_img)
            img.save(self.photo.path)


    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

class Subcategory(models.Model):
    title = models.CharField(max_length=200, verbose_name="Подкатегория", unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to='photos/subcategoria/', null=True)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (300, 250)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    def get_absolute_url(self):
        cat_id = Category.objects.filter(title=self.category).values()
        return reverse('subcategory', kwargs={'category_slug': cat_id[0]['slug'], 'subcategory_slug': self.slug})

class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategory, on_delete= models.CASCADE)
    recipe = models.TextField()
    cooking = models.TextField()
    photo = models.ImageField(upload_to='photos/product/')
    video = models.FileField(upload_to='video/')


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 50 or img.width > 50:
            new_img = (320, 250)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    def get_absolute_url(self):
        cat_id = Category.objects.filter(title=self.category).values()
        subcat_id = Subcategory.objects.filter(title=self.subcategoria).values()
        return reverse('product', kwargs={'category_slug': cat_id[0]['slug'], 'subcategory_slug': subcat_id[0]['slug'], 'product_slug': self.slug})


class Instruction(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    slug = models.CharField(max_length=255,unique=True)
    document = models.FileField(upload_to='document/')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instruction', kwargs={'slug_instruction': self.slug})

# блок тестов и вопросаов
class Test(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test', kwargs={'test': self.slug})

class Question(models.Model):
    question = models.TextField(null=True)
    answer = models.CharField(max_length=255)
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    right_one = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    
