from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import FreelancerProfile, ClientProfile

User = get_user_model()


@admin.action(description="Mark selected users as verified")
def mark_as_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    actions = [mark_as_verified]

    list_display  = ("email", "username", "role", "is_verified", "is_staff")
    list_filter   = ("role", "is_verified", "is_staff")
    search_fields = ("email", "username")
    ordering      = ("-date_joined",)
    
@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display  = ("user", "hourly_rate", "experience_years")
    search_fields = ("user__username", "user__email")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display  = ("user", "company_name", "website")
    search_fields = ("user__username", "user__email")
