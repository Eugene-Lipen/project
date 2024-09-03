from django.contrib import admin
from .models import Answer,Question, TestingCategory, TestingPeople

class TestingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}



class AnswersInLine(admin.TabularInline):
    model = Answer
    extra = 4

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id','text')
    list_display_links = ('id','text')
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersInLine]
    list_display = ('testing_category', 'text')
    list_display_links = ('testing_category', 'text')
    list_filter = ['testing_category','text']

class TestingPeopleAdmin(admin.ModelAdmin):
    list_display = ('test', 'people', 'attempt1', 'switch1', 'attempt2', 'switch2')
    list_display_links = ('test', 'people',)
    list_filter = ['test', 'people', 'attempt1', 'attempt2',]

admin.site.register(TestingPeople, TestingPeopleAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TestingCategory,TestingCategoryAdmin)
