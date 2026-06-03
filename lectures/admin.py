from django.contrib import admin
from .models import Subject, Chapter

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject',)
    prepopulated_fields = {'slug': ('title',)}
