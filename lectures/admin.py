from django.contrib import admin
from .models import Subject, Chapter, ContactMessage, QuestionAnswer, UserProfile, LoginAttempt, ChapterImage, Category, Topic

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order')
    list_filter = ('chapter__subject', 'chapter')
    search_fields = ('title',)

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 1
    readonly_fields = ('markdown_tag',)

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'topic_level', 'order')
    list_filter = ('subject',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TopicInline, ChapterImageInline]

@admin.register(ChapterImage)
class ChapterImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'chapter', 'markdown_tag_display')
    list_filter = ('chapter__subject', 'chapter')
    readonly_fields = ('markdown_tag_display',)

    def markdown_tag_display(self, obj):
        from django.utils.html import format_html
        return format_html('<code>{}</code>', obj.markdown_tag)
    markdown_tag_display.short_description = 'Markdown Tag (Copy this)'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('question', 'answer')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'security_question')
    search_fields = ('user__username', 'user__email', 'security_question')

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'failures', 'last_attempt')
    search_fields = ('username', 'ip_address')
    readonly_fields = ('last_attempt',)
