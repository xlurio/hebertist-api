from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import (
    GameModel, PriceModel, PriceHistoricModel, StoreModel, User, WishlistModel
)


class UserAdmin(BaseUserAdmin):
    """Defines the user forms in the admin interface"""
    # The forms to add and change users
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be displayed
    list_display = ['email', 'date_of_birth', 'is_staff']
    list_filter = ['is_staff']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ['date_of_birth']}),
        ('Permissions', {'fields': ['is_staff']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'date_of_birth', 'password1', 'password2']
        })
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


# Models registry
admin.site.register(GameModel)
admin.site.register(PriceModel)
admin.site.register(PriceHistoricModel)
admin.site.register(StoreModel)
admin.site.register(User, UserAdmin)
admin.site.register(WishlistModel)

admin.site.unregister(Group)
