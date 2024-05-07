from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Level)
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(Score)
admin.site.register(QuizSet)
admin.site.register(Quiz)