from django.contrib import admin
from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "last_message_at", "created_at")
    search_fields = ("phone_number", "summary")
    readonly_fields = ("created_at", "last_message_at")