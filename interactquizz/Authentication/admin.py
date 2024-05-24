from django.contrib import admin
from .models import *
# Register your models here.


class Options(admin.TabularInline):
    model = Option
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [Options]
    list_filter = ['subject']
    list_display = ["level", 'subject', 'quiz']

admin.site.register(Subject)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Level)
admin.site.register(CustomUser)
# admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(Score)
admin.site.register(Quiz)
