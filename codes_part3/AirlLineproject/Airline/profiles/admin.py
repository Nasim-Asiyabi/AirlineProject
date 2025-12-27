from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ['email', 'username', 'wallet_balance', 'is_staff']


    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات مالی و شخصی', {'fields': ('wallet_balance', 'phone_number', 'national_id')}),
    )


admin.site.register(User, CustomUserAdmin)