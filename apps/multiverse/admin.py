from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    max_num = 1
    
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)
    list_display = ('username', 'email', 'get_rank', 'is_staff')
    
    def get_rank(self, obj):
        return obj.profile.get_rank_display()
    get_rank.short_description = 'Rank'


# Registry
admin.site.unregister(User)
admin.site.register(User, UserAdmin)