from django.contrib import admin
from .models import Category, Subcategory, Product, Test, Question, Instruction, User, Work_Name
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth.admin import UserAdmin
from  .forms import CustomUserCreationForm


class Work_NameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Personal information',
            {
                'fields': (
                    'phone',
                    'telegram',
                    'date_job',
                    'position',
                    'turn_on_test',
                    'point',
                    'number_attempts'
                )
            }
        )
    )
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'telegram',  'is_active','date_joined')
    list_display_links = ('id', 'username')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'photo')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}

class ProductAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title',  'category', 'subcategoria')
    list_display_links = ('id', 'title')
    summernote_fields = ('recipe', 'cooking')
    prepopulated_fields = {"slug": ("title",)}

class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'test')
    list_display_links = ('id', 'question')

class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Instruction, InstructionAdmin)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Work_Name, Work_NameAdmin)
# Register your models here.
